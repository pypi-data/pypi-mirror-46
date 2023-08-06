#!/home/ubuntu/env/bin/python

###############################################################################
# charmmlipid2amber.py
# Version 2.0.3
# 2014-06-05
# Benjamin D. Madej
#
# Usage: 
# charmmlipid2amber.py [-c charmmlipid2amber.csv] -i input.pdb -o output.pdb
#
# Description:
# Processes PDB files for use with Lipid14. Default substitution file is in
# $AMBERHOME/AmberTools/src/etc. This program processes only ATOM, HETATM, and
# TER lines of a PDB file. Other lines will be removed from PDB.
###############################################################################

def charmmlipid2amber(input_file_name, output_file_name):

    amberhome = os.getenv('AMBERHOME')
    if amberhome == None:
        print "Error: charmmlipid2amber.py AMBERHOME not set and -c is not set. Set the AMBERHOME environment variable OR manually specify a substitution file with -c."
        print "Usage: charmmlipid2amber.py [-c charmmlipid2amber.csv] -i input.pdb -o output.pdb"
        sys.exit(2)
    else:
        # Hard coded into here. This has to be changed if the data file is moved.
        convert_file_name = "%s/dat/charmmlipid2amber/charmmlipid2amber.csv" % (amberhome)

    input_file  = open(input_file_name, 'r') # File to be processed
    input_file_list = [] # File to be processed as a list
    for line in input_file:
        input_file_list.append(line)
    input_file.close()

    # Process residues
    residue_list = [] # List of residue numbers
    residue_start = [] # List of lines where residues start. Line numbers start at 1.
    residue_end = [] # List of lines where residues end, including TER card if present. Line numbers start at 1.
    it0 = 1
    previous_residue = "" # Residue number of the previous line (including TER card). Set to "" if it is not an ATOM record or TER card.
    current_residue = "" # Residue number of the current line (including TER card). Set to "" if it is not an ATOM record or TER card.
    # Split file into residues by checking columns 23-27 (<99999 residues):
    # First line:
    if (input_file_list[0][0:6] == "ATOM  " or
        input_file_list[0][0:6] == "HETATM"):
        residue_list.append(input_file_list[0][22:27])
        residue_start.append(it0)
        previous_residue = input_file_list[0][22:27] 
    elif line[0:3] == "TER":
        previous_residue = ""
    else:
        previous_residue = ""
    it0+=1
    # Rest of lines:
    for line in input_file_list[1:]:
        if line[0:6] == "ATOM  " or line[0:6] == "HETATM":
            current_residue = line[22:27]
        elif line[0:3] == "TER":
            current_residue = previous_residue
        else:
            current_residue = ""
        if previous_residue != current_residue:
            # Previous line was not an ATOM or TER:
            if previous_residue == "":
                residue_list.append(current_residue)
                residue_start.append(it0)
                previous_residue = current_residue
            # Current line is not an ATOM or TER:
            elif current_residue == "":
                residue_end.append(it0-1)
                previous_residue = current_residue
            # Previous and current line are ATOM or TER:
            else:
                residue_list.append(current_residue)
                residue_start.append(it0)
                residue_end.append(it0-1)
                previous_residue = current_residue
        it0+=1
    # If the last residue is not closed, define the end:
    if current_residue != "":
        residue_end.append(it0-1)

    # Process substition dictionaries
    try:
        csv_file = open(convert_file_name, 'r') # csv file with all substitutions
    except IOError, err:
        print "Error: ", str(err)
        sys.exit(1)
    # Skip header line of csv file. Line 2 contains dictionary keys:
    csv_file.readline()
    csv_file_reader = csv.DictReader(csv_file) # Dictionary csv reader
    replace_dict = {} # Dictionary of atom name and residue name search and replace
    order_dict = {} # Dictionary of atom name and residue name order
    ter_dict = {} # Dictionary of whether residue should have a TER card based on atom name and residue name. All atom name and residue name in a residue with a TER card will return True.
    num_atom_dict = {} # Dictionary of number of atoms in current residue for the search string
    for line in csv_file_reader:
        replace_dict[line["search"]] = line["replace"]
        order_dict[line["search"]] = int(line["order"])
        ter_dict[line["search"]] = (line["TER"] == "True")
        num_atom_dict[line["search"]] = int(line["num_atom"])
    csv_file.close()

    # Do substitions
    # The search and replace is columns 13-21 in the PDB file:
    # 13-16: atom name
    # 17:      alternate location indicator
    # 18-20: residue name
    # 21:      sometimes used for the residue name
    output_file_list = [] # File to be written in list form (after processing)
    residue_substituted = False # For error checking. True if a substitution occurs.
    for it1 in range(0, len(residue_list)):
        # residue_start and residue_end indices start at 1. 
        # input_file_list indices start at 0.
        input_residue = input_file_list[residue_start[it1]-1:
            residue_end[it1]]
        output_residue = []
        # Process residue only if first atom is in the replacement dictionary:
        if input_residue[0][12:21] in replace_dict:
            residue_substituted = True
            # Check if length of input_residue is correct:
            # Count TER cards in residue for residue length arithmetic
            n_TER_cards = 0
            for line in input_residue:
                if line[0:3] == "TER":
                    n_TER_cards += 1
            if len(input_residue)-n_TER_cards != num_atom_dict[input_residue[0][12:21]]:
                print "Error: Number of atoms in residue does not match number of atoms in residue in replacement data file"
                sys.exit(1)
            output_residue = len(input_residue)*[0]
            for it2 in range(0, len(input_residue)):
                line = input_residue[it2]
                if line[0:3] != "TER":
                     search = line[12:21]
                     output_residue[order_dict[search]] = re.sub(search, 
                        replace_dict[search], line)
                else:
                     output_residue[it2] = "TER   \n"
            if ter_dict[input_residue[0][12:21]] == True:
                if input_residue[-1][0:3] != "TER":
                    output_residue.append("TER   \n")
        else:
            output_residue = input_residue
        output_file_list.extend(output_residue)
    # Check if any residues were substituted:
    if residue_substituted == False:
        print "Error: No residues substituted"
        sys.exit(1)

    resname_last = ''
    resnum_last = 0
    resum_new = 0
    new_output_file_list = []
    for line in output_file_list:
        if line.startswith(('ATOM', 'HETATM')):
            atomname = line[12:16].strip()
            resname = line[17:20].strip()
            resnum = int(line[22:27])
            if resname != resname_last or resnum != resnum_last:
                resum_new = (resum_new+1)%100000
            # (1) Add TER lines if needed
            if (resnum_last > resnum) or (resname == 'WAT' and atomname == 'O') or atomname in ['Na+', 'Cl-', 'K+']:
                new_output_file_list.append('TER\n')
            # (2) fix atom names
            if resname == 'ILE' and atomname == 'CD':
                atomname_new = ' CD1'
            else:
                atomname_new = line[12:16]
            # (3) fix residue names
            if resname == 'HSD':
                resname_new = 'HIS'
            else:
                resname_new = line[17:20]
            resname_last = resname
            resnum_last = resnum
            resum_new_str = str(resum_new)
            if len(resum_new_str) <= 4:
                resum_new_str = (4-len(str(resum_new)))*' ' + resum_new_str + ' '
            elif len(resum_new_str) == 5:
                resum_new_str = (5-len(str(resum_new)))*' ' + resum_new_str
            else:
                raise Exception("Something went wrong!")
            line_new = line[:12] + atomname_new + line[16:17] + resname_new + line[20:22] + resum_new_str + line[27:]
        else:
            line_new = line
        new_output_file_list.append(line_new)

    last_line = ''
    output_file_list = []
    for line in new_output_file_list:
        if not last_line.startswith('TER') or not line.startswith('TER'):
            output_file_list.append(line)
        last_line = line

    # Write output
    try:
        output_file = open(output_file_name, 'w') # File to be written
    except IOError, err:
        print "Error: ", str(err)
        sys.exit(1)
    for line in output_file_list:
        output_file.write(line)
    output_file.write("END   \n")
    output_file.close()
