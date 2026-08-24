from store import LastRecall
from datetime import datetime
# take the best rows and generate a list of n questions that I will email to myself
# need a few links that I can put in the email

def rank_questions(poss_review_problems, num_needed):
    # factors for consideration:
    # Last Recall Speed
    # Last Recall Confidence
    # Ratio of Num Consecutive Recalls : Num Recall Attempts
    # Next Review Date
    # ID number
    scores = []
    today = datetime.now()
    # (0.3 or 0.6 or 0.9) * (0.3 or 0.6 or 0.9)
    for row in poss_review_problems:
        score = row["Last Recall Confidence"].value * row["Last Recall Speed"].value
        score *= row["NumConsecutiveRecalls"] / row["NumRecallAttempts"]
        day_difference = (today - row["Next Review Date"]).days
        percentage = 1 / (1 + 0.01 * day_difference)
        score *= percentage
        scores.append([score, row["ID"]])

    target_idx = min(num_needed - 1, len(scores) - 1)
    if target_idx >= 0:
        quickselect(scores, 0, len(scores) - 1, target_idx)

    return scores[:num_needed]

def quickselect(arr, l, r, k):
    if l >= r:
        return arr[l]

    pivot_index = partition(arr, l, r)

    if pivot_index == k:
        return arr[pivot_index]
    elif k < pivot_index:
        return quickselect(arr, l, pivot_index - 1, k)
    else:
        return quickselect(arr, pivot_index + 1, r, k)

def partition(arr, l, r):
    pivot = arr[r]
    store = l
    for i in range(l, r):
        if arr[i] <= pivot:
            arr[i], arr[store] = arr[store], arr[i]
            store += 1

    arr[store], arr[r] = arr[r], arr[store]
    return store

# the idea for this comes from knowing that if I am struggling with a pattern I am more likely to not be confident in problems surrounding the "lowest" earliest problem
def rank_questions_binary_search(poss_review_problems, num_needed):
    pass


def first_n_new(all_rows, num_needed):
    new_problems = []
    for row in all_rows[1:]:
        if num_needed <= 0:
            break
        if not row['Last Recall Confidence']:
            new_problems.append(row)
            num_needed -= 1

    return new_problems