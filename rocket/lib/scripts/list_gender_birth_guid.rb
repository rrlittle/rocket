$LOAD_PATH.unshift(__dir__)

require 'rdoc_utils'

uRSIForTest = 'M53779169'
initLogger(true)
initPiggybank

if ARGV[0] != nil
	puts "I'm in the first branch"

	ARGV.each do |argv|
		ursi = argv
		individual = $piggybank.get_demographics_by_ursi(ursi)

		tags = $piggybank.get_tags_by_ursi(ursi)
		guid = tags["RDoC GUID"]
		wbic = tags["WBIC"]
		if (guid.nil?)
			guid = "NONE"
		end
		if (wbic.nil?)
			wbic = "NONE"
		end

		puts  "{\'" + ursi + "\':{\'gender\': \'"+ individual.gender + "\',\'birth_date\':\'" + individual.birth_date+ "\',\'GUID\':\'" + guid+  "\'}}" 
	end

else
	puts "I'm in the second branch"
	
	subjects = $piggybank.list_subjects 8200
	subjects.each do  |subject|
		ursi = subject.ursi 
		individual = $piggybank.get_demographics_by_ursi(ursi)

		tags = $piggybank.get_tags_by_ursi(ursi)
		guid = tags["RDoC GUID"]
		wbic = tags["WBIC"]
		if (guid.nil?)
			guid = "NONE"
		end
		if (wbic.nil?)
			wbic = "NONE"
		end

		puts  "{\'" + ursi + "\':{\'gender\': \'"+ individual.gender + "\',\'birth_date\':\'" + individual.birth_date+ "\',\'GUID\':\'" + guid+  "\'}}" 
	end
end