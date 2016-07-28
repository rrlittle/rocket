#!/usr/bin/env ruby
#
# rdoc_utils.rb
#
# Assorted utility functions used by the various scripts which create 
# RDoCdb-upload-ready spreadsheets. These utilities include
# routines to wrap and log Piggybank calls, open and read commonly-used files, 
# and do various conversions.

# $LOAD_PATH.unshift(File.dirname(__FILE__)+"/lib")
# Prepend Piggybank to the Ruby load path. Note that Piggybank needs to be 
# on the same drive (letter)
# as this script!
$LOAD_PATH.unshift(__dir__ + "/../piggybank/lib")

# Hack in case Ruby doesn't have the latest certificates and/or the COINS 
# certificate is out
# of date. Ruby crashes either way, but yeah, we trust the COINS server, 
# so tell Ruby to relax
# and just get the $^%&&*$ data.
require 'openssl'
I_KNOW_THAT_OPENSSL_VERIFY_PEER_EQUALS_VERIFY_NONE_IS_WRONG = nil
OpenSSL::SSL.send(:remove_const, :VERIFY_PEER)
OpenSSL::SSL.const_set(:VERIFY_PEER, OpenSSL::SSL::VERIFY_NONE)

require 'logger'
require 'pp'
require 'csv'
require 'chronic'
require 'piggybank'


DEFAULT_USER_SKIPPED_CODE = 77
DEFAULT_COINS_SKIPPED_CODE = -99
DEFAULT_MISSING_CODES = [DEFAULT_USER_SKIPPED_CODE, DEFAULT_COINS_SKIPPED_CODE]


# Fire up the logger

def initLogger(debugOn = false)
	$logger = Logger.new(STDOUT)
	if debugOn
		$logger.level = Logger::DEBUG
	else
		$logger.level = Logger::INFO
	end
	return $logger
end


# Comparison of 2 fields both taken from .CSV files or databases. They may 
# be strings or integers or whatnot,
# upper or lower case. So try to convert them both to strings and downcase 
# them; give them the best chance
# of matching. Return true if they pretty much match, false otherwise.

def compareFields(fieldA, fieldB)
	a = fieldA.to_s.strip.downcase
	b = fieldB.to_s.strip.downcase
	$logger.debug { "compareFields: comparing '" + a + "' to '" + b + "'..." }
	if (a == b)
		$logger.debug { "   They match!" }
		return true
	end
	$logger.debug { "    NO match!" }
	return false
end


# Comparison of two Time fields. If they match, return true, otherwise false.

def compareTimes(dateA, dateB)
	$logger.debug { "compareTimes: comparing '" 
			+ dateA.to_s + "' to '" + dateB.to_s + "'..." }
	if (dateA == dateB)
		$logger.debug { "   They match!" }
		return true
	end
	$logger.debug { "    NO match!" }
	return false
end


# find all the files with the given extension fileExtension in 
# mamaDirectory and its one-or-two-levels-down subdirs

def findFiles(mamaDirectory, fileExtension)
	$logger.debug { ": Looking for '" + fileExtension + "' in '" +
		mamaDirectory + "' ..." }
	# Rather than get all recursive, just check a couple levels down.
	# If the files aren't within those levels, there's a problem.
	extFiles = Dir.glob mamaDirectory + "/*" + fileExtension
	extFiles += Dir.glob mamaDirectory + "/*/*" + fileExtension
	extFiles += Dir.glob mamaDirectory + "/*/*/*" + fileExtension
	if (extFiles.size <= 0)
		$logger.debug { "    No files found!" }
		return nil;
	end
	return extFiles
end


# Convert a string to a Time object and log it.

def convertStringToTime(s)
	$logger.debug { "convertStringToTime: converting '" + s + "'..." }
	t = Chronic.parse(s)
	$logger.debug { "    ... to " + t.to_s }
	return t
end


# Do the initialization of Piggybank and login into COINS.
def initPiggybank
	begin
		$piggybank = Piggybank.logged_in_from_file
	rescue Errno::ENOENT
		$logger.error { "Can't find your shell file. Log in to COINS, visit:" }
		$logger.error { "https://chronus.mrn.org/micis/admin/index.php?action"+
			"=niGetFile&DoCSV=true" }
		$logger.error { "and save that in your home directory as niGet_sh.key" }
		$logger.fatal { "Exiting." }
  	end
	$logger.debug { "Successfully logged into COINS." }
end


# Given a Study ID, return a list of subject URSIs in the study with the 
# 'RDoC GUID' and 'WBIC' tags for each URSI.

def getGUIDURSIWBIC(studyID)
	tags = $piggybank.list_subjects(studyID)
	tags.each_with_index do |subj, index|
		tags[index] = [$piggybank.get_tags(subj)["RDoC GUID"], subj.ursi, 
						$piggybank.get_tags(subj)["WBIC"]]
	end
	
	return tags
end


# Given an URSI, return the equivalent GUID or nil if no GUID for this URSI.

def URSI2GUID(thisURSI)
	$logger.debug { "URSI2GUID: looking for GUID for URSI: " + thisURSI }

	tags = $piggybank.get_tags_by_ursi thisURSI
	if tags.nil? or tags.size < 1
		$logger.warn { "    Couldn't find URSI '" + thisURSI +
			"' tags data in COINS!" }
	 	return nil
	end
	$logger.debug { "    Tags: '" + tags.to_s + "'." }

	return tags["RDoC GUID"]
end


# Given an URSI, return the equivalent GUID and WBIC tags, or nil if either 
# GUID or WBIC is missing for this URSI.

def URSI2GUIDandWBIC(thisURSI)
	$logger.debug { "URSI2GUIDandWBIC: looking for GUID and WBIC for URSI: " 
		+ thisURSI }

	tags = $piggybank.get_tags_by_ursi thisURSI
	if tags.nil? or tags.size < 1
		$logger.warn { "    Couldn't find URSI '" + thisURSI +
			"' tags data in COINS!" }
	 	return [nil, nil]
	end

	return [tags["RDoC GUID"], tags["WBIC"]]
end


# Given an URSI, return the subject's PPI date of birth, gender. Or nil
# dob is a Time object. gender is a String.

def URSI2PPI(thisURSI)
	$logger.debug { "URSI2PPI: looking for PPI for URSI: " + thisURSI }

	subject = $piggybank.get_demographics_by_ursi thisURSI
	if subject.first_name == nil
		$logger.warn { "    Couldn't find URSI '" + thisURSI +
			"' demographics data in COINS!" }
	 	return [nil, nil]
	end
  	dob = convertStringToTime(subject.birth_date)

	return [dob, subject.gender]
end


# Run the COINS Query Builder on the given instrument
# Returns true if run succeeds, false if not.
# This doesn't currently work.

def runQueryBuilder(studyID, instrumentID)
	results = $piggybank.get_query_builder_results(STUDY_ID, INSTRUMENT_ID)
	return true
end


# Find the newest COINS export "coinsExport_...tsv" file in the
# specified directory and return it's full pathname.

def newestCOINSExportTSV(mamaDirectory = ".")
	$logger.debug { "newestCOINSExportTSV: Looking for .TSV in '" +
		mamaDirectory + "' ..." }
	tsvFiles = Dir.glob mamaDirectory + "/coinsExport*/*tsv"
	if (tsvFiles.size <= 0)
		$logger.debug { "    No .TSV files found!" }
		return nil;
	end
	byNewestFiles = tsvFiles.sort_by {|fileName| File.mtime(fileName) }.reverse
	$logger.debug { "    Returning .TSV file: '" +
		byNewestFiles[0].to_s + "'." }
	return byNewestFiles[0]
end





# Assign a string read in from a COINS .TSV file to the corresponding NDAR 
# equivalent integer.
# Check if it's user-skipped, cond-skipped, or outside the valid minValid -
 # maxValid range,
# and return the correspoinding code if so. Otherwise return the valid 
# integer value.
# 
def assignCOINSvalueToNDARvalue(coinsValue, minValid, maxValid,
		userSkippedCode = DEFAULT_USER_SKIPPED_CODE, 
		coinsSkippedCode = DEFAULT_COINS_SKIPPED_CODE)
	
	$logger.debug { "assignCOINSvalueToNDARvalue(" + coinsValue.to_s + "," 
		+ minValid.to_s + "," + maxValid.to_s + "," +
		userSkippedCode.to_s + "," + coinsSkippedCode.to_s + ")" }
	if coinsValue == "~<userSkipped>~"
		$logger.debug { "    returning user-skipped." }
		return userSkippedCode
	elsif coinsValue == "~<condSkipped>~"
		$logger.debug { "    returning COINS-skipped." }
		return coinsSkippedCode
	end
	
	ndarValue = coinsValue.to_i
	
	if (ndarValue < minValid) or (ndarValue > maxValid)
		$logger.debug { "    invalid value; returning COINS-skipped." }
		return coinsSkippedCode
	end
	
	$logger.debug { "    returning " + ndarValue.to_s + "." }
	return ndarValue
end


# Compute the sum for a list of numbers, SPSS-style, by handling missing 
# numbers and complaining if
# too many are missing.
#
# Inputs:
#	nums: Array of numbers.
#	minNonMissing: minimum number of 'nums' that are needed to compute a valid sum. Expressed either as
#		an integer (1 or higher), or a percentage (0.0 through 0.9999). Defaults to 80%.
#	missingCodes: Array of values in 'nums' that indicate a missing values. 'nums' set to any of these values will
#		be included in the computation.
#
# Return value: float that's the sum of the numbers in 'nums', or -9999.00.



def sumWithMissing(nums, minNonMissing = 0.8, 
	missingCodes = DEFAULT_MISSING_CODES)
		if nums.nil? or nums.size < 1
			$logger.debug { "sumWithMissing: Invalid input"
				+ " array of numbers! Returning -9999.99" }
			return -9999.00
		end
		if minNonMissing.to_f < 1.0
			f = minNonMissing * nums.size.to_f
			maxMissing = nums.size - f.round.to_i
		else
			maxMissing = nums.size - minNonMissing.to_i
		end
		$logger.debug { "sumWithMissing: Array of " + nums.size.to_s 
			+ "numbers. Maximum missing = " + maxMissing.to_s }
		thisSum = 0.0
		numMissing = 0
		nums.each do |thisNum|
			if missingCodes.include? thisNum
				numMissing += 1
				if (numMissing >= maxMissing)
					$logger.debug { "    Too many missing numbers."
						+ " Returning -9999.00" }
					return -9999.00
				end
			else
				thisSum += thisNum.to_f
			end
		end
		
		# Prorate the sum to account for missing values.
		if numMissing >= 1
			thisSum = thisSum * nums.size.to_f / (nums.size - numMissing).to_f
		end
		
		$logger.debug { "    Returning " + thisSum.to_s }
		return thisSum
end


# Compute the mean for a list of numbers, SPSS-style, by handling 
# missing numbers and complaining if
# too many are missing.
#
# Inputs:
#	nums: Array of numbers.
#	minNonMissing: minimum number of 'nums' that are needed to compute a
# valid sum. Expressed either as
#		an integer (1 or higher), or a percentage (0.0 through 0.9999). 
# Defaults to 80%.
#	missingCodes: Array of values in 'nums' that indicate a missing values. 
# 'nums' set to any of these values will
#		be included in the computation.
#
# Return value: float that's the mean of the numbers in 'nums', or -9999.00.


def meanWithMissing(nums, minNonMissing = 0.8, missingCodes = DEFAULT_MISSING_CODES)
		if nums.nil? or nums.size < 1
			$logger.debug { "sumWithMissing: Invalid input array of numbers! Returning -9999.99" }
			return -9999.00
		end
		if minNonMissing.to_f < 1.0
			f = minNonMissing * nums.size.to_f
			maxMissing = nums.size - f.round.to_i
		else
			maxMissing = nums.size - minNonMissing.to_i
		end
		$logger.debug { "meanWithMissing: Array of " + nums.size.to_s 
			+ "numbers. Maximum missing = " + maxMissing.to_s }
		thisSum = 0.0
		numMissing = 0
		nums.each do |thisNum|
			if missingCodes.include? thisNum
				numMissing += 1
				if (numMissing >= maxMissing)
					$logger.debug { "    Too many missing numbers. "
						+ "Returning -9999.00" }
					return -9999.00
				end
			else
				thisSum += thisNum.to_f
			end
		end
		divisor = nums.size - numMissing
		if (divisor < 1)
			return -9999.00
		end
		result = thisSum / divisor.to_f
		$logger.debug { "    Returning " + result.to_s }
		return result
end


# Unit tests.

if __FILE__ == $0
	initLogger(true)
	
    nums = [1, 2, 3, 4, 5, 6, -99, 77, -99, 7, 8, 9]
	mNM = 5
	mC = [-99]
	puts sumWithMissing(nums).to_s
	puts sumWithMissing(nums, mNM).to_s
	puts sumWithMissing(nums, nums.size - 4)
	
	puts meanWithMissing(nums).to_s
	puts meanWithMissing(nums, mNM).to_s
	puts meanWithMissing(nums, nums.size - 4)
	
end