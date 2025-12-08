package math

func Product(values []int) int {
	/*
		The go stdlib really doesn't have a product() function.
	*/

	if len(values) == 0 {
		return 0
	}

	result := 1
	for _, val := range values {
		result *= val
	}
	return result
}
