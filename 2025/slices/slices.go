package iter

func Map[T any, U any](values []T, transform func(T) U) []U {
	/*
	   The go stdlib really doesn't have a map() function.
	*/

	result := make([]U, len(values))
	for i, val := range values {
		result[i] = transform(val)
	}
	return result
}
