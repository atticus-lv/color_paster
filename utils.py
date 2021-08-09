import re
import colorsys

# rule to match, HSL match with %number
rules = {
    'HEX': r'^#?[a-fA-F\d]{6}$',
    'RGB': r'^[rR][gG][Bb][Aa]?[\(]([\s]*(2[0-4][0-9]|25[0-5]|[01]?[0-9][0-9]?),){2}[\s]*(2[0-4][0-9]|25[0-5]|[01]?[0-9][0-9]?),?[\s]*(0\.\d{1,2}|1|0)?[\)]{1}$',
    'HSL': r'^[Hh][Ss][Ll][\(](((([\d]{1,3}|[\d\%]{2,4})[\,]{0,1})[\s]*){3})[\)]',
    'RGB_pure': r'^([\s]*(2[0-4][0-9]|25[0-5]|[01]?[0-9][0-9]?),){2}[\s]*(2[0-4][0-9]|25[0-5]|[01]?[0-9][0-9]?),?[\s]*(0\.\d{1,2}|1|0)?$',
    # 'HSV':'[Hh][Ss][Vv][\(](((([\d]{1,3}|[\d\%]{2,4})[\,]{0,1})[\s]*){3})[\)]'
}


class ColorPicker():
    def __init__(self, clipboard):
        self.clipboard = clipboard

    @property
    def bl_color(self):
        ans = self.match_rule()
        if not ans: return

        rule, string = ans

        if rule == 'HEX':
            return self.Hex_to_RGBA(string)
        elif rule in {'RGB', 'RGB_pure'}:
            return self.RGB_to_RGB(string, has_prefix=True if rule == 'RGB' else False)
        elif rule == 'HSL':
            return self.HSL_to_RGB(string)

    def match_rule(self):
        for k, v in rules.items():
            m_obj = re.match(v, self.clipboard)
            if m_obj: return k, m_obj.group(0)

    # gamma correct method
    #########################

    def sRGB_to_linearRGB(self, c):
        """https://blender.stackexchange.com/questions/158896/how-set-hex-in-rgb-node-python?noredirect=1#comment269316_158896"""
        if c < 0:
            return 0
        elif c < 0.04045:
            return c / 12.92
        else:
            return ((c + 0.055) / 1.055) ** 2.4

    # convert method
    #########################

    def Hex_to_RGBA(self, hex_str, alpha=1):
        if hex_str.startswith('#'): hex_str = hex_str[1:]

        hex = eval(f'0x{hex_str}')
        r = (hex & 0xff0000) >> 16
        g = (hex & 0x00ff00) >> 8
        b = (hex & 0x0000ff)

        return tuple([self.sRGB_to_linearRGB(c / 0xff) for c in (r, g, b)] + [alpha])

    def RGB_to_RGB(self, rgb_str, alpha=1, has_prefix=True):
        rgb = [c / 255 for c in eval(rgb_str[3:] if has_prefix else rgb_str)]
        rgb = [self.sRGB_to_linearRGB(c) for c in rgb]

        if len(rgb) == 3: rgb.append(alpha)
        return rgb

    def HSL_to_RGB(self, hsl_str, alpha=1):
        hsl_str = hsl_str.replace('%', '')
        hsl = [c for c in eval(hsl_str[3:])]
        hsl = colorsys.hls_to_rgb(hsl[0], hsl[2] / 100, hsl[1] / 100)
        hsl = [self.sRGB_to_linearRGB(c) for c in hsl]
        hsl.append(alpha)
        return hsl
