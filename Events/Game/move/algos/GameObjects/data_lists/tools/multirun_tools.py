import math


def get_std(list_of_valuse):
    mean = get_mean(list_of_valuse)

    sum_of_squares_deviations=0
    for iteration_value in list_of_valuse:
        sum_of_squares_deviations=sum_of_squares_deviations+math.pow(iteration_value-mean,2)

    std=math.sqrt(float(sum_of_squares_deviations)/len(list_of_valuse))


    return std


def get_mean(list_of_valuse):
    sum = 0
    for iteration_value in list_of_valuse:  # calculate sum of points for all iterations
        sum = sum + iteration_value
    mean = float(sum) / len(list_of_valuse)
    return mean
