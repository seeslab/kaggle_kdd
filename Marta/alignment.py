from Bio.pairwise2 import align

# -----------------------------------------------------------------------------

# Given two strings, return the score of the alignment. The score is
# the ratio between the number of matched letters and the total length
# of the alignment. Case, hyphens, and spaces are ignored in the
# alignment.

# -----------------------------------------------------------------------------
def clean(theString):
    return theString.upper().replace('-','').replace(' ','')

def string_align_score(s1, s2):
    alignment = align.globalxx(clean(s1), clean(s2))
    print alignment
    maxScore = 0.0
    for an_al in alignment:
        score = float(an_al[2]) / float(an_al[4])
        if score > maxScore:
            maxScore = score

    return maxScore


if __name__ == '__main__':
    s1 = 'Roger Guimera'
    s2 = 'R Guimera'
    print string_align_score(s1, s2)
