import sys
import os

def translator(file):
    score = 0
    best_score = 0
    gap = 0

    for line in file:

        # Finishes when it reaches the reverse part
        if 'Reverse' in line:
            break
        
        if 'Errors' in line:
            if best_score < score:
                #print(seqA, seqB, score)
                best_score = score
            score = 0

        # First sequence
        if line[0] == "A":
            seqA = (line[:-1])[3:]

        # Second sequence
        elif line[0] == "B":
            seqB = (line[:-1])[3:]

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
                
                #print(seqA[i], seqB[i], score, gap)

    return best_score    

def main():
    command = "run-mummer3 " + str(sys.argv[1]) + " " + str(sys.argv[2]) + " " + str(sys.argv[3])
    os.system(command)
    
    print("\n\nFinding and translating the best score...\n")
    file_name = (str(sys.argv[3]) + ".align")
    f = open(file_name, "r")
    score = translator(f)
    print('Translated score:', score, "\n\n")

if __name__ == "__main__":
    main()
