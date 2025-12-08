package vector

import (
	"math"
)

// TODO: how can we genericize the number of dimensions?
type Vector3 [3]float64

func (self Vector3) Magnitude() float64 {
	sum := 0.0
	for _, val := range self {
		sum += math.Pow(val, 2)
	}
	return math.Pow(sum, 0.5)
}

func (self Vector3) Minus(other Vector3) Vector3 {
	result := Vector3{}
	for i := range self {
		result[i] = self[i] - other[i]
	}
	return result
}
