"""
    This file should contain the function that works for getting data from wtp_data database about personal information.
    Couple assumptions need to be clarified:
       1: GUID information will not get pulled from the coinsPersonal.tmp, it should get data direct from database
          table: gen_rdmr_guid.
          if twin number is 3, then it's a caregiver.

       2: Gender and DOB information will also not get pulled from coinsPersonal.tmp. It should get data direct
          from "gen_twin" for twin. (But I don't know where pull data from for caregiver)

       3: use pyodbc to connect with the database, DSN = wtp_data

       4: each operation will open a connection and close at the end (Let's change if there is performance issue)

"""

from Functions.function_api import Function, DropRowFunction
from Managers import ssManager
import pyodbc
from dateutil import relativedelta
from datetime import datetime

guid_table = "gen_rdmr_guid"
rdoc_info = "user_jj_rdoc_ppt_info"
def get_open_connection():
    return pyodbc.connect("DSN=wtp_data")


class FindGuidByWTPInt(Function):
    """
        This function accepts two possible keys: one is the combination of familyid and twin, and the other is just
         familyid

        The first combination will be seen as twin, suggesting that their twin number will be either 1 or 2
        The second option will be seen as caregiver, suggesting that its twin number will be 3 in gen_family_guid

    """

    def get_name(self):
        return "findGuidByWTPInt"

    def get_documentation(self):
        return super().get_documentation()

    def _func_(self, data_list, args=None):

        if len(data_list) != 1 and len(data_list) !=2:
            raise Exception("data_list should be length of 1 or 2")

        if len(data_list) == 1:
            return self._get_guid_for_familyid_and_twin(familyid=data_list[0], twin=3)
        else:
            return self._get_guid_for_familyid_and_twin(familyid=data_list[0], twin=data_list[0])

    def _get_guid_for_familyid_and_twin(self, familyid, twin):
        con = get_open_connection()
        cur = con.cursor()
        cur.execute("SELECT guid from {0} WHERE familyid = '{1}' AND twin = {2}".format(guid_table, familyid, twin))
        rows = cur.fetchmany()
        if len(rows) > 1:
            raise Exception("Duplicate guid for caregiver. familyid: {0}".format(familyid))
        if len(rows) == 0:
            raise Exception("No guid for familyid: %s, twin: %s" %(familyid, twin))
        con.close()
        # example rows will look like this [('NDARDM306PUU',)]
        return rows[0][0]


class FindGenderByWTPInt(Function):

    # this mapping defines how to translate our database coding to NDAR requirement
    gender_mapping = {
        1 : "F",
        2 : "M",
        9998 : ssManager.NoDataError("Empty gender")
    }

    def _func_(self, data_list, args=None):
        if len(data_list) != 1 and len(data_list) !=2:
            raise Exception("data_list should be length of 1 or 2")

        if len(data_list) == 1:
            # Use data_r1_tr to decide the gender for caregiver
            gender = self._get_gender_(familyid=data_list[0], twin=3)
            return self.gender_mapping[int(gender)]
        else:
            gender = self._get_gender_(familyid=data_list[0], twin=data_list[1])
            return self.gender_mapping[int(gender)]

    def _get_gender_(self, familyid, twin):
        con = get_open_connection()
        cur = con.cursor()
        sql = "SELECT gender FROM {0} WHERE familyid = '{1}' AND twin = {2}".format(rdoc_info, familyid, twin)
        cur.execute(sql)

        rows = cur.fetchmany()
        if len(rows) > 1:
            raise Exception("Duplicate gender for caregiver. familyid: {0}".format(familyid))
        if len(rows) == 0:
            raise Exception("No guid for familyid: %s, twin: %s" % (familyid, twin))
        con.close()
        return rows[0][0]


    def get_documentation(self):
        return "Find gender given the familyid and twin or just familyid. Twin should always follow familyid"

    def get_name(self):
        return "findGenderByWTPInt"


class FindAgeByWTPInt(Function):
    """
        This functions represents the function that gets the age for a twin or caregiver based on the key
        It fetches the assessment date from data_r1_tr column "twadps". It fetches the dob from gen_twin column dateofbirth
        for twin.
        Then use the function to calculate the age.

    """

    def get_name(self):
        return "findAgeByWTPInt"

    def _func_(self, data_list, args=None):
        if len(data_list) != 1 and len(data_list) !=2:
            raise Exception("data_list should be length of 1 or 2")

        if len(data_list) == 1:
            # decide parent gender
            # then decide whether i should mother dob or father dob
            #
            dob_date = self._get_birth_date_ (familyid=data_list[0], twin=3)

            if dob_date is None:
                return ssManager.NoDataError()

            assessment = self._get_assessment_date_(familyid=data_list[0])
            return self._calculate_age_(dob_date, assessment)

        else:

            dob_date = self._get_birth_date_(familyid=data_list[0], twin=data_list[1])
            if dob_date is None:
                return ssManager.NoDataError()
            assessment_date = self._get_assessment_date_(familyid=data_list[0])
            return self._calculate_age_(dob_date,assessment_date)

    def _get_gender_for_cg_(self, familyid):
        con = get_open_connection()
        cur = con.cursor()
        sql = "SELECT pc FROM data_r1_tr WHERE familyid = '{0}' AND datamode = 'Entry';".format(familyid)
        cur.execute(sql)

        rows = cur.fetchmany()
        if len(rows) > 1:
            raise Exception("Duplicate gender for caregiver. familyid: {0}".format(familyid))
        if len(rows) == 0:
            raise Exception("No guid for familyid: %s" % familyid)
        con.close()
        return rows[0][0]

    def _get_birth_date_(self, familyid, twin):
        con = get_open_connection()
        cur = con.cursor()
        sql = "SELECT dateofbirth FROM {0} WHERE familyid = '{1}' AND twin = {2} ;".format(rdoc_info, familyid, twin)
        cur.execute(sql)
        rows = cur.fetchmany()
        if len(rows) > 1:
            raise Exception("Duplicate dob for twin: familyid: {0}, twin: {1}".format(familyid, twin))
        if len(rows) == 0:
            raise Exception("No dob for familyid: %s" % familyid)
        con.close()
        date_string = rows[0][0]
        if date_string == "9998":
            raise Exception("NoDOBDataForParticipant")
        return datetime.strptime(date_string, '%m/%d/%Y')

    def _get_birth_date_twin(self, familyid, twin):
        con = get_open_connection()
        cur = con.cursor()
        sql = "SELECT dateofbirth FROM gen_twins WHERE familyid = '{0}' AND twin = {1};".format(familyid, twin)
        cur.execute(sql)
        rows = cur.fetchmany()
        if len(rows) > 1:
            raise Exception("Duplicate dob for twin: familyid: {0}, twin: {1}".format(familyid, twin))
        if len(rows) == 0:
            raise Exception("No dob for familyid: %s, twin: %s" % (familyid, twin))
        con.close()
        date_string = rows[0][0]

        if date_string == "9998":
            raise Exception("NoDOBDataForParticipant")

        return datetime.strptime(date_string, '%m/%d/%Y')

    def _get_assessment_date_(self, familyid):
        con = get_open_connection()
        cur = con.cursor()
        sql = "SELECT twadps FROM data_r1_tr WHERE familyid = '{0}';".format(familyid)
        cur.execute(sql)
        rows = cur.fetchmany()
        if len(rows) > 1:
            raise Exception("Duplicate dob for twin: familyid: {0}".format(familyid))
        if len(rows) == 0:
            raise Exception("No guid for familyid: %s " %familyid)
        con.close()
        date_string = rows[0][0]

        if date_string == "9998":
            raise Exception("NoAssessDataForParticipant")

        return datetime.strptime(date_string, '%m/%d/%Y')

    def _calculate_age_(self, olddate, recentdate):
        age = relativedelta.relativedelta(olddate, recentdate)
        year = abs(age.years)
        month = abs(age.months)
        day = abs(age.days)
        if day > 15:
            month = month + 1

        total_months = year * 12 + month
        return total_months

    def get_documentation(self):
        return "return the age given the familyid and twin or just familyid. Twin should always follow familyid"


