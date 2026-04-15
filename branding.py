from textwrap import dedent


def get_morepen_logo_html(compact: bool = False) -> str:
    """Return an inline SVG/HTML brand block for the MOREPEN logo."""
    if compact:
        return dedent(
            """
            <div style="background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%); border: 1px solid #dbe7f3; border-radius: 16px; padding: 18px 16px 14px; margin-bottom: 14px; box-shadow: 0 8px 24px rgba(30, 41, 59, 0.06);">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <svg width="54" height="54" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" aria-label="Morepen logo mark">
                        <g fill="none" stroke-linecap="round" stroke-width="14">
                            <path d="M60 17 C60 33, 46 33, 46 47" stroke="#1939D6"/>
                            <path d="M103 60 C87 60, 87 46, 73 46" stroke="#1AB9E0"/>
                            <path d="M60 103 C60 87, 74 87, 74 73" stroke="#1939D6"/>
                            <path d="M17 60 C33 60, 33 74, 47 74" stroke="#1AB9E0"/>
                            <path d="M60 17 C60 33, 74 33, 74 47" stroke="#1939D6"/>
                            <path d="M103 60 C87 60, 87 74, 73 74" stroke="#1AB9E0"/>
                            <path d="M60 103 C60 87, 46 87, 46 73" stroke="#1939D6"/>
                            <path d="M17 60 C33 60, 33 46, 47 46" stroke="#1AB9E0"/>
                        </g>
                        <g fill="#1939D6">
                            <circle cx="60" cy="17" r="9"/>
                            <circle cx="17" cy="60" r="9" fill="#1AB9E0"/>
                            <circle cx="60" cy="103" r="9"/>
                            <circle cx="103" cy="60" r="9" fill="#1AB9E0"/>
                            <circle cx="37" cy="37" r="9"/>
                            <circle cx="83" cy="37" r="9"/>
                            <circle cx="37" cy="83" r="9"/>
                            <circle cx="83" cy="83" r="9" fill="#1AB9E0"/>
                        </g>
                    </svg>
                    <div>
                        <div style="font-family: 'Montserrat', sans-serif; font-size: 1.5rem; font-weight: 800; letter-spacing: 0.04em; color: #1939D6; line-height: 1;">MOREPEN</div>
                        <div style="font-family: 'Georgia', serif; font-size: 0.68rem; letter-spacing: 0.18em; color: #1f2937; margin-top: 6px;">
                            PROPRIETARY DRUG RESEARCH
                        </div>
                    </div>
                </div>
            </div>
            """
        ).strip()

    return dedent(
        """
        <div style="text-align: center; margin: 6px 0 20px;">
            <div style="display: inline-flex; align-items: center; gap: 18px; padding: 12px 18px; background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%); border: 1px solid #dbe7f3; border-radius: 22px; box-shadow: 0 12px 32px rgba(30, 41, 59, 0.08);">
                <svg width="96" height="96" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" aria-label="Morepen logo mark">
                    <g fill="none" stroke-linecap="round" stroke-width="14">
                        <path d="M60 17 C60 33, 46 33, 46 47" stroke="#1939D6"/>
                        <path d="M103 60 C87 60, 87 46, 73 46" stroke="#1AB9E0"/>
                        <path d="M60 103 C60 87, 74 87, 74 73" stroke="#1939D6"/>
                        <path d="M17 60 C33 60, 33 74, 47 74" stroke="#1AB9E0"/>
                        <path d="M60 17 C60 33, 74 33, 74 47" stroke="#1939D6"/>
                        <path d="M103 60 C87 60, 87 74, 73 74" stroke="#1AB9E0"/>
                        <path d="M60 103 C60 87, 46 87, 46 73" stroke="#1939D6"/>
                        <path d="M17 60 C33 60, 33 46, 47 46" stroke="#1AB9E0"/>
                    </g>
                    <g fill="#1939D6">
                        <circle cx="60" cy="17" r="9"/>
                        <circle cx="17" cy="60" r="9" fill="#1AB9E0"/>
                        <circle cx="60" cy="103" r="9"/>
                        <circle cx="103" cy="60" r="9" fill="#1AB9E0"/>
                        <circle cx="37" cy="37" r="9"/>
                        <circle cx="83" cy="37" r="9"/>
                        <circle cx="37" cy="83" r="9"/>
                        <circle cx="83" cy="83" r="9" fill="#1AB9E0"/>
                    </g>
                </svg>
                <div style="text-align: left;">
                    <div style="font-family: 'Montserrat', sans-serif; font-size: 3.25rem; font-weight: 800; letter-spacing: 0.05em; color: #1939D6; line-height: 0.95;">
                        MOREPEN
                    </div>
                    <div style="font-family: 'Georgia', serif; font-size: 0.95rem; letter-spacing: 0.24em; color: #1f2937; margin-top: 12px;">
                        PROPRIETARY DRUG RESEARCH
                    </div>
                </div>
            </div>
        </div>
        """
    ).strip()
