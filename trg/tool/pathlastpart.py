
class PathLastPart:
    def pathlastpart_(self, path_):
        if path_.find('/') != -1:
            idx1 = path_.rindex('/', 0, len(path_)) + 1
        else:
            idx1 = 0
        if path_.find('\\') != -1:
            idx2 = path_.rindex('\\', 0, len(path_)) + 1
        else:
            idx2 = 0
        idx = max(idx1, idx2)
        lastpart = path_[idx:]
        return lastpart