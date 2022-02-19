import sys
import os

def translator():
    print("\n\nFinding and translating the MUMmer best alignment score...\n")    
    file = open("result.align", "r")
    score = 0
    best_score = 0
    gap = 0
    best_align = []
    align = []

    for line in file:

        # Finishes when it reaches the reverse part
        if 'Reverse' in line:
            break
        
        if 'Errors' in line:
            if best_score < score:
                #print(seqA, seqB, score)
                best_score = score
                best_align = align
            score = 0
            align = []

        # First sequence
        if line[0] == "A":
            seqA = (line[:-1])[3:]
            align.append(line[:-1])

        # Second sequence
        elif line[0] == "B":
            seqB = (line[:-1])[3:]
            align.append(line)

            # Compare each nucleobase between sequences
            for i in range(len(seqA)):

                # Match
                if seqA[i] == seqB[i]:
                    score += 1
                    gap = 0

                # Gap
                elif seqA[i] == "-" or seqB[i] == "-":
                    # Opening
                    if gap == 0:
                        score -= 5
                        gap = 1
                    # Extension
                    else:
                        score -= 2
                
                # Mismatch
                elif seqA[i] != seqB[i]:
                    score -= -3
                    gap = 0
                
            #print(seqA, seqB, score, gap)

    for line in best_align:
        print(line)

    file.close()

    return best_score

def finder():
    file = open("result.lastz.maf", "r")
    print("\n\nFinding the Lastz best alignment score...\n")

    best = 0

    for line in file:
        if "a score=" in line and best < int((line[:-1])[8:]):
            best = int((line[:-1])[8:])
    
    file.close()

    return best

def script_modifier(score):
    f = open("sbatch-nvidia-2", "r")
    script_lines = f.readlines()
    f.close()
    for line in range(len(script_lines)):
        if "score=" in script_lines[line]:
            script_lines[line] = f"score={score}\n"
    f = open("sbatch-nvidia-2", "w")
    new_script = "".join(script_lines)
    f.write(new_script)
    f.close() 

def main():

    score = -1

    if str(sys.argv[1]) == "-h":
        print("\nOptions:\nExecute with MUMmer:\npython3 score_translator.py -m dir sequence1.fasta sequence2.fasta\n\nExecute with Lastz:\npython3 score_translator.py -l dir sequence1.fasta sequence2.fasta [traceback]\n")
        print("Note: traceback must be bigger than 0\n\tdir must be in format 1-3m\n")

    elif str(sys.argv[1]) == "-m":
        command = f"run-mummer3 {str(sys.argv[3])} {str(sys.argv[4])} result"
        os.system(command)
        score = translator()
        print(f"Translated score: {score} \n\n")

    elif str(sys.argv[1] == "-l"):
        command = f"lastz {str(sys.argv[3])} {str(sys.argv[4])} --scores=scores_lastz_sw --strand=plus --gapped --hspthresh=100000 ‑‑allocate:traceback={str(sys.argv[5])}.0M --format=maf+ > result.lastz.maf"
        os.system(command)
        score = finder()
        print(f"Found score: {score}\n\n")

    if score != -1:
        script_modifier(score)
        command =f"sbatch sbatch-nvidia-2 {str(sys.argv[2])}"
        print(command)

if __name__ == "__main__":
    main()