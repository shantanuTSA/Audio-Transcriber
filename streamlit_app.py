def highlight_text(segments):
    highlighted = ""

    for seg in segments:
        text = seg["text"]
        conf = seg["confidence"]

        # 🔴 Low confidence
        if conf < -1.0:
            highlighted += f"<span style='color:red'>{text}</span> "

        # 🟡 Medium confidence
        elif conf < -0.5:
            highlighted += f"<span style='color:orange'>{text}</span> "

        # 🟢 High confidence
        else:
            highlighted += f"<span style='color:green'>{text}</span> "

    return highlighted