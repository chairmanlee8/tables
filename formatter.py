Normal = 0

# negation style flags
Accounting = 1

# alignment flags
Left = 0
Right = 1
Center = 2

class TextFormatter:
    def __init__(self, align=Left):
        self.align = align

    def format_all(self, heading, values):
        max_width = max(len(heading), *map(len, values))
        return [
            "{:{align}{width}}".format(value, 
                align=('', '>')[self.align], 
                width=max_width
            )
            for value in values
        ]

class NumberFormatter(TextFormatter):
    def __init__(self, fmt=Normal, precision=None, comma='', point='.', 
            prefix='', negation=Normal, whole=False, align=Right, 
            decimal_align=False):
        super().__init__(align)
        self.fmt = fmt
        self.precision = precision
        self.comma = comma
        self.point = point
        self.prefix = prefix
        self.negation = negation
        self.whole = whole
        self.decimal_align = decimal_align

    def baseformat(self, value):
        base = str(abs(value))
        l, r = base.split('.') if '.' in base else (base, '')
        l = l[::-1]
        ls = [l[i:i+3][::-1] for i in range(0, len(l), 3)][::-1]
        
        if self.precision is not None:
            r = r[:self.precision]
            # pad right to get desired precision
            if len(r) < self.precision:
                r += "0" * (self.precision - len(r))

        x = self.comma.join(ls)
        return (x, '' if self.whole else r)

    def internalalign(self, base_formats):
        if self.whole:
            return [x for x, _ in base_formats]
        elif self.decimal_align:
            max_whole_width = max(*(len(x) for x, _ in base_formats))
            max_frac_width = max(*(len(r) for _, r in base_formats))
            max_width = max_whole_width + 1 + max_frac_width

            return [
                "%*s%s%s" % (max_whole_width, x, self.point, r)
                for x, r in base_formats
            ]
        else:
            return [self.point.join([x, r]) for x, r in base_formats]

    def sign(self, s, is_negative):
        if self.negation == Accounting: 
            return "(" + s + ")" if is_negative else " " + s + " "
        else: 
            return "-" + s if is_negative else " " + s

    # TODO: change heading to heading_width
    def format_all(self, heading, values):
        base = self.internalalign([self.baseformat(v) for v in values])
        string_values = [
            self.prefix + self.sign(s, v < 0) 
            for s, v in zip(base, values)
        ]

        return super().format_all(heading, string_values)

