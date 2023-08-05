def version_compare(ver1, ver2):
    if ver1 > ver2:
        return "{0} Version is greater than Version {1}".format(ver1, ver2)
    elif ver1 == ver2:
        return "{0} Version is equal to Version {1}".format(ver1, ver2)
    elif ver1 < ver2:
        return "{0} Version is lesser than Version {1}".format(ver1, ver2)


if __name__ == '__main__':
    try:
        ver1 = float(input('Please enter first value of Version number: \n'))
        ver2 = float(input('Please enter second value of Version number: \n'))
        result = version_compare(ver1, ver2)
        print(result)

    except ValueError:
        print('\nPlease enter numeric value, no other value is valid')