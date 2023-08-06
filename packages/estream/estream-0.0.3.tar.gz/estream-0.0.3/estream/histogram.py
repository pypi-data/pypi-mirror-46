from copy import deepcopy
from sys import maxsize

class Histogram:

    """
    Constructor
    """
    def __init__(self,
                 has_min=False, has_max=False,
                 min_val=-maxsize, max_val=maxsize, size=10,
                 width=0.0, heights=None, upper_bounds=None,
                 significant=3.843, sensitivty=5):
        # Public fields
        self.has_min = has_min
        self.has_max = has_max
        self.min = min_val
        self.max = max_val
        self.size = size
        self.width = width
        self.heights = [height for height in heights] if heights is not None else [0.0] * size
        self.upper_bounds = [upper_bound for upper_bound in upper_bounds] if upper_bounds is not None else [0.0] * size
        # Private fields
        self.__significant = significant
        self.__sensitivity = sensitivty
    
    """
    Overridden Methods
    """
    def __copy__(self):
        return self.__clone()
    
    def __deepcopy__(self, memo):
        copy = self.__clone()
        copy.heights = deepcopy(self.heights, memo)
        copy.upper_bounds = deepcopy(self.upper_bounds, memo)

        return copy
    
    """
    Public methods
    """
    def add(self, value, height=1.0):
        if not self.has_min:
            self.has_min = True

            self.min = value
            self.heights[0] = height
        elif not self.has_max:
            if value < self.min:
                self.has_max = True

                self.max = self.min
                self.min = value
                self.heights[-1] = self.heights[0]
                self.heights[0] = height

                self.__update_interval()
            elif value > self.min:
                self.has_max = True

                self.max = value
                self.heights[-1] = height

                self.__update_interval()
            else:
                self.heights[0] += height
        else:
            if value < self.min:
                self.min = value

                self.__update()
            elif value > self.max:
                self.max = value

                self.__update()
            
            i = next(idx for idx, upper_bound in enumerate(self.upper_bounds)
                     if value <= upper_bound)
            self.heights[i] += height
    
    def merge(self, other):
        if not self.has_min or not other.has_min:
            raise ValueError('Cannot merge empty histogram(s)!')

        if self.has_max:
            if other.has_max:
                new_min = min(self.min, other.min)
                new_max = max(self.max, other.max)

                self.min, self.max = new_min, new_max
                other.min, other.max = new_min, new_max
                self.__update()
                other.__update()
                self.heights = [height_1 + height_2 for height_1, height_2
                                in zip(self.heights, other.heights)]
            else:
                self.add(other.min, other.heights[0])
        else:
            if other.has_max:
                other.add(self.min, self.heights[0])
                
                self.__dict__.update(other.__dict__)
            else:
                self.add(other.min, other.heights[0])
    
    def split(self, index):
        if index == -1:
            return None
        
        left_w, right_w = 0, 0
        for idx, height in enumerate(self.heights):
            if idx <= index:
                left_w += height
            else:
                right_w += height
        
        new_histogram = Histogram(has_min=self.has_min, has_max=self.has_max, size=self.size,
                                  width=self.width, upper_bounds=self.upper_bounds,
                                  significant=self.__significant, sensitivty=self.__sensitivity)
        if left_w > right_w:
            new_histogram.min = self.upper_bounds[index]
            new_histogram.max = self.max
            new_histogram.heights = [height if idx > index else 0.0
                                     for idx, height in enumerate(self.heights)]
            self.max = self.upper_bounds[index]
        else:
            new_histogram.min = self.min
            new_histogram.max = self.upper_bounds[index]
            new_histogram.heights = [height if idx <= index else 0.0
                                     for idx, height in enumerate(self.heights)]
            self.min = self.upper_bounds[index]
        new_histogram.__update()
        self.__update()

        return new_histogram
    
    def find_split_index(self):
        index, split_index = -1, -1
        first_peek, second_peek = -1.0, -1.0
        valley, min_valley = -1.0, -1.0
    
        def __is_significant():
            observed, expected = valley, (valley + min(first_peek, second_peek)) / 2

            return (valley < min_valley or split_index == -1) \
                and 2 * ((observed - expected) ** 2) / expected >= self.__significant
        
        def __update_min_valley():
            nonlocal split_index, first_peek, min_valley, state

            if __is_significant():
                min_valley = valley
                split_index = index

            if second_peek > first_peek:
                state = 1

                first_peek = second_peek

        state = 0
        for idx, height in enumerate(self.heights):
            if state == 0:
                if height > first_peek and height >= self.__sensitivity:
                    first_peek = height
                elif height < first_peek:
                    state = 1

                    valley = height
                    index = idx
            elif state == 1:
                if height < valley:
                    valley = height
                    index = idx
                elif height > valley:
                    state = 2

                    second_peek = height
                    __update_min_valley()
            elif state == 2:
                if idx == self.size - 1 and height > second_peek and height >= self.__sensitivity:
                    second_peek = height
                    __update_min_valley()
                elif height > second_peek and height >= self.__sensitivity:
                    second_peek = height
                elif height < second_peek and height < valley:
                    valley = height
                    index = idx
                    __update_min_valley()
            
        return split_index
    
    """
    Private methods
    """
    def __clone(self):
        cls = self.__class__
        clone = cls.__new__(cls)
        clone.__dict__.update(self.__dict__)

        return clone

    def __update(self):
        old_width = self.width
        old_heights = [height for height in self.heights]
        old_upper_bounds = [upper_bound for upper_bound in self.upper_bounds]

        self.__update_interval()

        new_lower_bound, new_upper_bound = self.min, self.min + self.width
        old_lower_bound, old_upper_bound = old_upper_bounds[0] - old_width, old_upper_bounds[0]
        new_i, old_i = 0, 0
        self.heights = [0.0] * self.size
        while new_i < self.size and old_i < self.size:
            if new_lower_bound < old_lower_bound:
                if new_upper_bound > old_lower_bound:
                    if new_upper_bound < old_upper_bound:
                        intersection = new_upper_bound - old_lower_bound
                        self.heights[new_i] += old_heights[old_i] * intersection / old_width

                        new_i += 1
                        new_lower_bound += self.width
                        new_upper_bound += self.width
                    else:
                        self.heights[new_i] += old_heights[old_i]

                        old_i += 1
                        old_lower_bound += old_width
                        old_upper_bound += old_width
                else:
                    new_i += 1
                    new_lower_bound += self.width
                    new_upper_bound += self.width
            else:
                if new_lower_bound < old_upper_bound:
                    if new_upper_bound > old_upper_bound:
                        intersection = old_upper_bound - new_lower_bound
                        self.heights[new_i] += old_heights[old_i] * intersection / old_width

                        old_i += 1
                        old_lower_bound += old_width
                        old_upper_bound += old_width
                    else:
                        self.heights[new_i] += old_heights[old_i] * self.width / old_width

                        new_i += 1
                        new_lower_bound += self.width
                        new_upper_bound += self.width
                else:
                    old_i += 1
                    old_lower_bound += old_width
                    old_upper_bound += old_width
    
    def __update_interval(self):
        self.width = (self.max - self.min) / self.size
        self.upper_bounds = [self.min + self.width * (idx + 1) if idx < self.size - 1 else self.max
                             for idx in range(self.size)]
