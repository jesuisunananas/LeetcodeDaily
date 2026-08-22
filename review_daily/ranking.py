from store import LastRecall
# take the best rows and generate a list of n questions that I will email to myself
# need a few links that I can put in the email

def rank_questions(poss_review_problems, num_needed):
    # factors for consideration:
    # Last Recall Speed
    # Last Recall Confidence
    # Ratio of Num Consecutive Recalls : Num Recall Attempts
    # Next Review Date
    # ID number
    problems_to_review = []

    

    return problems_to_review

# the idea for this comes from knowing that if I am struggling with a pattern I am more likely to not be confident in problems surrounding the "lowest" earliest problem
def rank_questions_binary_search(poss_review_problems, num_needed):
    


def first_n_new(all_rows, num_needed):
    new_problems = []
    for row in all_rows:
        if num_needed <= 0:
            break
        if not row['Last Recall Confidence']:
            new_problems.append(row)
            num_needed -= 1

    return new_problems