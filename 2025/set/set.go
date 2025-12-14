package set

import (
	"maps"
)

type Set[T comparable] map[T]struct{}

func Make[T comparable](values []T) Set[T] {
	set := make(Set[T], len(values))
	for _, val := range values {
		set.Add(val)
	}
	return set
}

func (self Set[T]) Add(value T) {
	self[value] = struct{}{}
}

func (self Set[T]) Remove(value T) {
	delete(self, value)
}

func (self Set[T]) Has(value T) bool {
	_, ok := self[value]
	return ok
}

func (self Set[T]) Clone() Set[T] {
	return maps.Clone(self)
}

func (self Set[T]) Iter() func(yield func(T) bool) {
	return func(yield func(T) bool) {
		for value := range self {
			still_going := yield(value)
			if !still_going {
				return
			}
		}
	}
}

func (self Set[T]) Union(other Set[T]) Set[T] {
	union := self.Clone()
	for value := range other.Iter() {
		union.Add(value)
	}
	return union
}
