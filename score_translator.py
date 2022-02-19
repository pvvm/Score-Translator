import sys
import os

def translator(file):
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

    return best_score

def finder(file):

    best = 0

    for line in file:
        if "a score=" in line and best < int((line[:-1])[8:]):
            best = int((line[:-1])[8:])
    
    return best

def main():

    if str(sys.argv[1]) == "-h":
        print("\nOptions:\nExecute with MUMmer:\npython3 score_translator.py -m sequence1.fasta sequence2.fasta\n\nExecute with Lastz:\npython3 score_translator.py -l sequence1.fasta sequence2.fasta [traceback]\n")
        print("Note: traceback must be bigger than 0\n\n")

    elif str(sys.argv[1]) == "-m":
        command = f"run-mummer3 {str(sys.argv[2])} {str(sys.argv[3])} result"
        os.system(command)
        print("\n\nFinding and translating the MUMmer best alignment score...\n")    
        f = open("result.align", "r")
        score = translator(f)
        print(f"Translated score: {score} \n\n")

    elif str(sys.argv[1] == "-l"):
        command = f"lastz {str(sys.argv[2])} {str(sys.argv[3])} --scores=scores_lastz_sw --strand=plus --gapped --hspthresh=100000 ‑‑allocate:traceback={str(sys.argv[4])}.0M --format=maf+ > result.lastz.maf"
        os.system(command)
        f = open("result.lastz.maf", "r")
        print("\n\nFinding the Lastz best alignment score...\n")
        score = finder(f)
        print(f"Found score: {score}\n\n")

    #command = f"./cudalign --clear --stage-1 --blocks=512 --mummer-score={score} --no-flush {str(sys.argv[2])} {str(sys.argv[3])}"
    #os.system(command)

if __name__ == "__main__":
    main()