class Cube:

    _dataLower = [
        "a", "b", "c", "d", "e",
        "f", "g", "h", "i", "j",
        "k", "l", "m", "n", "o",
        "p", "q", "r", "s", "t",
        "u", "v", "w", "z", "y"
    ]

    _dataUpper = [x.upper() for x in _dataLower]

    def __init__(self, size=5):
        self.size = size
        self.x1_index = -1
        self.y1_index = -1
        self.x2_index = -1
        self.y2_index = -1
        self.result = ""
        self._makeScaleArray(size)
        pass

    def __del__(self):
        pass

    def _makeScaleArray(self, size):
        count = 0
        self.dataLower = [["" for x in range(size)] for y in range(size)]
        for x in range(size):
            for y in range(size):
                self.dataLower[x][y] = self._dataLower[count]
                count += 1

    def insertX(self, inputO, output, i = 0):
        output = output + inputO[i]
        if i == len(inputO) - 1:
            self.result = output
            return
        if inputO[i] == inputO[i + 1]:
            output = output + "X"
        self.insertX(inputO, output, i + 1)

    def encrypt(self, sentence):
        final_sentence = ""
        output = ""
        temp = sentence
        sentence = ""
        for x in temp:
            sentence += x.lower()
        self.insertX(sentence, output)

        sentence = self.result

        for counter in range(0, len(sentence), 2):
            two = [x for x in sentence[counter:counter+2]]
            two = [x for x in two]
            if len(two) < 2:
                final_sentence += two[0]
                continue
            self._findXandY(two)
            if self.x1_index != self.x2_index and self.y1_index != self.y2_index:
                if self.y2_index != -1 and self.x2_index != -1 and self.y1_index != -1 and self.x1_index != -1:
                    if two[0] != " " and two[1] != " ":
                        temp = self.y1_index
                        self.y1_index = self.y2_index
                        self.y2_index = temp
                        two[0] = self.dataLower[self.y1_index][self.x1_index]
                        two[1] = self.dataLower[self.y2_index][self.x2_index]
                    print(two)
                final_sentence += two[0] + two[1]
            elif self.x1_index == self.x2_index and self.y1_index != self.y2_index:
                if self.y2_index != -1 and self.x2_index != -1 and self.y1_index != -1 and self.x1_index != -1:
                    if two[0] != " " and two[1] != " ":
                        self.x1_index += 1
                        self.x2_index += 1
                        if self.x1_index >= len(self.dataLower):
                            self.x1_index = 0
                        if self.x2_index >= len(self.dataLower):
                            self.x2_index = 0
                        two[0] = self.dataLower[self.y1_index][self.x1_index]
                        two[1] = self.dataLower[self.y2_index][self.x2_index]
                    print(two)
                final_sentence += two[0] + two[1]
            elif self.y1_index == self.y2_index and self.x1_index != self.x2_index:
                if self.y2_index != -1 and self.x2_index != -1 and self.y1_index != -1 and self.x1_index != -1:
                    if two[0] != " " and two[1] != " ":
                        self.y1_index += 1
                        self.y2_index += 1
                        if self.y1_index >= len(self.dataLower):
                            self.y1_index = 0
                        if self.y2_index >= len(self.dataLower):
                            self.y2_index = 0
                        two[0] = self.dataLower[self.y1_index][self.x1_index]
                        two[1] = self.dataLower[self.y2_index][self.x2_index]
                    print(two)
                final_sentence += two[0] + two[1]
            else:
                final_sentence += two[0] + two[1]
                pass
        if len(final_sentence) % 2 == 1:
            final_sentence += "X"

        return final_sentence

    def _findXandY(self, two):
        temp = True
        self.x1_index = -1
        self.y1_index = -1
        self.x2_index = -1
        self.y2_index = -1
        for y in range(len(self.dataLower)):
            for x in range(len(self.dataLower)):
                if self.dataLower[y][x] == two[0]:
                    self.x1_index = x
                    self.y1_index = y
                    temp = False
                    break

        for y in range(len(self.dataLower)):
            for x in range(len(self.dataLower)):
                if self.dataLower[y][x] == two[1]:
                    self.x2_index = x
                    self.y2_index = y
                    temp = False
                    break
        return temp

    def checkUpper(self, letter):
        return 'A' <= letter <= 'Z'

    def decrypt(self, sentence):
        final_sentence = ""
        for counter in range(0, len(sentence), 2):
            two = [x for x in sentence[counter:counter + 2]]
            if len(two) < 2:
                final_sentence += two[0]
                continue
            two = [x for x in two]
            self._findXandY(two)
            if two[0] == "X" or two[1] == "X":
                final_sentence += two[0] + two[1]
                continue
            if self.x1_index != self.x2_index and self.y1_index != self.y2_index:
                if self.y2_index != -1 and self.x2_index != -1 and self.y1_index != -1 and self.x1_index != -1:
                    if two[0] != " " and two[1] != " ":
                        temp = self.y1_index
                        self.y1_index = self.y2_index
                        self.y2_index = temp
                        two[0] = self.dataLower[self.y1_index][self.x1_index]
                        two[1] = self.dataLower[self.y2_index][self.x2_index]
                final_sentence += two[0] + two[1]
            elif self.x1_index == self.x2_index and self.y1_index != self.y2_index:
                if self.y2_index != -1 and self.x2_index != -1 and self.y1_index != -1 and self.x1_index != -1:
                    if two[0] != " " and two[1] != " ":
                        self.x1_index -= 1
                        self.x2_index -= 1
                        if self.x1_index < 0:
                            self.x1_index = len(self.dataLower) - 1
                        if self.x2_index < 0:
                            self.x2_index = len(self.dataLower) - 1
                        two[0] = self.dataLower[self.y1_index][self.x1_index]
                        two[1] = self.dataLower[self.y2_index][self.x2_index]
                final_sentence += two[0] + two[1]
            elif self.y1_index == self.y2_index and self.x1_index != self.x2_index:
                if self.y2_index != -1 and self.x2_index != -1 and self.y1_index != -1 and self.x1_index != -1:
                    if two[0] != " " and two[1] != " ":
                        self.y1_index -= 1
                        self.y2_index -= 1
                        if self.y1_index < 0:
                            self.y1_index = len(self.dataLower) - 1
                        if self.y2_index < 0:
                            self.y2_index = len(self.dataLower) - 1
                        two[0] = self.dataLower[self.y1_index][self.x1_index]
                        two[1] = self.dataLower[self.y2_index][self.x2_index]
                final_sentence += two[0] + two[1]
            else:
                final_sentence += two[0] + two[1]
                pass
        return final_sentence
        pass
