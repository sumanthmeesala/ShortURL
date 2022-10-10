class ShortURLService:
    def __init__(self):
        self.chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.charsLength = len(self.chars)
        self.length = 6

    def idToShortURL(self, id: int):
        shortLink = 'a' * self.length
        for i in range(self.length - 1, -1, -1):
            shortLink = shortLink[:i] + self.chars[int(id % self.charsLength)] + shortLink[i + 1:]
            id /= self.charsLength
        return shortLink

    def shortURLToID(self, shortLink) -> int:
        id = 0
        for c in shortLink:
            id *= self.charsLength
            if 'a' <= c <= 'z':
                id += ord(c) - ord('a')
            elif 'A' <= c <= 'Z':
                id += ord(c) - ord('A') + 26
            elif '0' <= c <= '9':
                id += ord(c) - ord('0') + 52

        return id
