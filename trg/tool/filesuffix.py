
class FileSuffix:
    def filesuffix_(self, filename_):
        if filename_.find('.') != -1:
            idx = filename_.rindex('.', 0, len(filename_)) + 1
        else:
            idx = len(filename_)
        suffix = filename_[idx:]

        return suffix