class BusinessMetrics():
    
    # Positive Count
    def count_pos_neg(df):
        tot = len(df.index)
        pos = df['sentiment'].str.count("pos").sum() / tot * 100
        neg = df['sentiment'].str.count("neg").sum() / tot * 100
        res = {
            "positive": pos, 
            "negative": neg
        }
        return res

    # Ratio of Pos to Neg
    def pos_neg_ratio(df):
        pos = df['sentiment'].str.count("pos").sum()
        neg = df['sentiment'].str.count("neg").sum()
        r1 = pos // neg
        r2 = neg // pos
        if r1 > r2:
            return str(r1) + ":1"
        return "1:" + str(r2)
        return "%s" % float((pos/r) / (pos/r))

    # Extract Hashtags
    def extract_hashtags(text):
        res = ''.join(re.findall("(?:\s|^)#[A-Za-z0-9\-\.\_]+(?:\s|$)", text, re.S))
        return res

    # Extract Keywords
    def extract_keywords(df):
        pass