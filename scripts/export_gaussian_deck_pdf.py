#!/usr/bin/env python3
"""
scripts/export_gaussian_deck_pdf.py
Sinh trực tiếp file PDF trình chiếu Digital vs. Analog Reliable Signal Science Presentation.pdf (16:9 Widescreen)
chuẩn xác 5 slide theo đúng chuẩn thiết kế Canva (Orange Top, Cyan Bottom, Clean White Canvas)
và cắt ảnh từng slide bằng pdftoppm phục vụ Visual QA.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg

# Palette màu chuẩn từ template Canva
C_WHITE = "#FFFFFF"
C_CARD_BG = "#F8FAFC"
C_CYAN = "#00BCD4"        # Cyan chuẩn Canva
C_CYAN_ACCENT = "#00A8FF" # Tech Cyan
C_CYAN_DARK = "#0284C7"
C_ORANGE = "#FF9800"      # Orange chuẩn Canva
C_ORANGE_DARK = "#C2410C"
C_SLATE_DARK = "#0F172A"
C_SLATE_MUTED = "#475569"
C_BORDER = "#CBD5E1"
C_HUD_DARK = "#333333"

OUT_PDF = Path("Digital vs. Analog Reliable Signal Science Presentation.pdf")
MEDIA_DIR = Path("build/unpacked_patched/ppt/media")
OUT_IMG_DIR = Path("assets/presentation")
OUT_IMG_DIR.mkdir(parents=True, exist_ok=True)
TOTAL_SLIDES = 5

def create_slide_base(slide_num, total_slides=TOTAL_SLIDES):
    # Kích thước 16:9 widescreen: 13.333 x 7.5 inches
    fig = plt.figure(figsize=(13.333, 7.5), facecolor=C_WHITE, dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.set_xlim(0, 13.333)
    ax.set_ylim(0, 7.5)

    # Top Orange Accent Stripe (Canva Theme)
    top_bar = patches.Rectangle((0, 7.15), 13.333, 0.35, facecolor=C_ORANGE, edgecolor="none")
    ax.add_patch(top_bar)

    # Bottom Dark Slate Sub-line
    bot_dark = patches.Rectangle((0, 0.30), 13.333, 0.08, facecolor=C_HUD_DARK, edgecolor="none")
    ax.add_patch(bot_dark)

    # Bottom Cyan Accent Stripe
    bot_bar = patches.Rectangle((0, 0), 13.333, 0.30, facecolor=C_CYAN, edgecolor="none")
    ax.add_patch(bot_bar)

    # Slide Footer Text
    footer_text = f"XỬ LÝ TÍN HIỆU SỐ — THUẬT TOÁN 3: GAUSSIAN BAYES  |  SLIDE {slide_num}/{total_slides}"
    ax.text(12.7, 0.15, footer_text, fontsize=9.5, color=C_WHITE, ha="right", va="center", fontweight="bold")

    return fig, ax

def add_header(ax, title, subtitle=None):
    ax.text(0.7, 6.70, title.upper(), fontsize=20, fontweight="bold", color=C_CYAN_ACCENT, va="center")
    if subtitle:
        ax.text(0.7, 6.30, subtitle, fontsize=12.5, fontweight="medium", color=C_SLATE_MUTED, va="center")

# -------------------------------------------------------------
# SLIDE 1: COVER
# -------------------------------------------------------------
def build_slide_1(pdf):
    fig, ax = create_slide_base(1)

    # Big Title
    ax.text(6.666, 4.70, "PHÂN ĐOẠN TIẾNG NÓI\nVÀ KHOẢNG LẶNG (VAD)", 
            fontsize=36, fontweight="bold", color=C_CYAN_ACCENT, ha="center", va="center", linespacing=1.2)

    # Subtitle
    ax.text(6.666, 3.45, "Thuật toán 3: Phân phối chuẩn Gaussian & Ngưỡng tối ưu Bayes T*", 
            fontsize=17, fontweight="bold", color=C_ORANGE_DARK, ha="center", va="center")

    # Info Card
    card = patches.FancyBboxPatch((2.2, 1.4), 8.933, 1.45, boxstyle="round,pad=0.08,rounding_size=0.15",
                                  facecolor=C_CARD_BG, edgecolor=C_BORDER, linewidth=1.5)
    ax.add_patch(card)

    ax.text(6.666, 2.25, "Báo cáo Giữa kỳ môn Xử lý Tín hiệu Số (XLTHS 2026)", 
            fontsize=14, fontweight="bold", color=C_SLATE_DARK, ha="center", va="center")
    ax.text(6.666, 1.75, "Nhóm 14  •  Thời lượng trình bày: 03 Phút  •  Dataset: 4 Train / 4 Test", 
            fontsize=13, color=C_SLATE_MUTED, ha="center", va="center")

    pdf.savefig(fig)
    plt.close()

# -------------------------------------------------------------
# SLIDE 2: QUY TRÌNH 4 GIAI ĐOẠN
# -------------------------------------------------------------
def build_slide_2(pdf):
    fig, ax = create_slide_base(2)
    add_header(ax, "QUY TRÌNH THUẬT TOÁN 3: PHÂN ĐOẠN GAUSSIAN BAYES", 
               "Pipeline 4 giai đoạn khép kín từ trích xuất đặc trưng năng lượng đến định vị biên thời gian")

    stages = [
        ("STAGE 01", "Phân Khung & STE", "• Cửa sổ 20ms, trượt 10ms\n• Tính năng lượng STE\n• Chuẩn hóa dải [0, 1]"),
        ("STAGE 02", "Ước Lượng Tham Số", "• Tách Speech vs Silence\n• Ước lượng μ và σ\n• Xây dựng 2 hàm PDF"),
        ("STAGE 03", "Ngưỡng Bayes T*", "• Lập pt Bayes Quadratic\n• Tìm giao điểm phân bố\n• Ngưỡng T* = 0.002495"),
        ("STAGE 04", "Hậu Xử Lý & Đánh Giá", "• Khử khoảng lặng <200ms\n• Trích xuất biên thời gian\n• Đánh giá MAE & RMSE"),
    ]

    x_start = 0.7
    card_w = 2.8
    card_gap = 0.24

    for i, (tag, title, body) in enumerate(stages):
        cx = x_start + i * (card_w + card_gap)
        
        # Outer Card
        card = patches.FancyBboxPatch((cx, 1.0), card_w, 4.9, boxstyle="round,pad=0.08,rounding_size=0.15",
                                      facecolor=C_CARD_BG, edgecolor=C_CYAN if i%2==0 else C_ORANGE, linewidth=1.8)
        ax.add_patch(card)

        # Stage Badge
        badge = patches.FancyBboxPatch((cx + 0.35, 5.25), card_w - 0.7, 0.45, boxstyle="round,pad=0.04,rounding_size=0.1",
                                       facecolor=C_CYAN if i%2==0 else C_ORANGE, edgecolor="none")
        ax.add_patch(badge)
        ax.text(cx + card_w/2, 5.47, tag, fontsize=12, fontweight="bold", color=C_WHITE, ha="center", va="center")

        # Card Title
        ax.text(cx + card_w/2, 4.65, title, fontsize=14, fontweight="bold", color=C_SLATE_DARK, ha="center", va="center")

        # Separator line
        ax.plot([cx + 0.4, cx + card_w - 0.4], [4.3, 4.3], color=C_BORDER, lw=1.0)

        # Card Body (<= 10 words/line)
        ax.text(cx + 0.25, 2.7, body, fontsize=12, color=C_SLATE_DARK, va="center", linespacing=1.6)

    pdf.savefig(fig)
    plt.close()

# -------------------------------------------------------------
# SLIDE 3: HUẤN LUYỆN & PDF GAUSSIAN
# -------------------------------------------------------------
def build_slide_3(pdf):
    fig, ax = create_slide_base(3)
    add_header(ax, "HUẤN LUYỆN PHÂN BỐ GAUSSIAN & NGƯỠNG TỐI ƯU T*", 
               "Ước lượng tham số (μ, σ) từ 4 file Train và tìm điểm giao nhau xác suất Bayes Quadratic")

    # Embed Image 18 (Gaussian PDF)
    img_path = MEDIA_DIR / "image18.png"
    if img_path.exists():
        img = mpimg.imread(str(img_path))
        ax.imshow(img, extent=[0.7, 12.633, 2.1, 5.95], aspect="auto", zorder=2)

    # Caption Box 1 (Left - Subplot a)
    c1 = patches.FancyBboxPatch((0.7, 0.75), 5.7, 1.15, boxstyle="round,pad=0.06,rounding_size=0.1",
                                facecolor=C_CARD_BG, edgecolor=C_BORDER, linewidth=1.2)
    ax.add_patch(c1)
    ax.text(0.95, 1.50, "• Lặng (Silence): μ = 0.00025, σ = 0.00063 (phân bố hẹp sát 0)", 
            fontsize=11, fontweight="bold", color=C_SLATE_DARK, va="center")
    ax.text(0.95, 1.10, "• Tiếng nói (Speech): μ = 0.20247, σ = 0.23569 (phân tán rộng)", 
            fontsize=11, fontweight="bold", color=C_SLATE_DARK, va="center")

    # Caption Box 2 (Right - Subplot b)
    c2 = patches.FancyBboxPatch((6.933, 0.75), 5.7, 1.15, boxstyle="round,pad=0.06,rounding_size=0.1",
                                facecolor=C_CARD_BG, edgecolor=C_BORDER, linewidth=1.2)
    ax.add_patch(c2)
    ax.text(7.183, 1.50, "• Nghiệm Bayes: p(x|Silence) = p(x|Speech) → T* = 0.002495", 
            fontsize=11, fontweight="bold", color=C_ORANGE_DARK, va="center")
    ax.text(7.183, 1.10, "• Giao điểm tối ưu: Cân bằng xác suất phân loại nhầm giữa 2 lớp", 
            fontsize=11, color=C_SLATE_DARK, va="center")

    pdf.savefig(fig)
    plt.close()

# -------------------------------------------------------------
# SLIDE 4: BẢNG ĐỊNH LƯỢNG
# -------------------------------------------------------------
def build_slide_4(pdf):
    fig, ax = create_slide_base(4)
    add_header(ax, "KẾT QUẢ ĐÁNH GIÁ ĐỊNH LƯỢNG TRÊN 4 TỆP KIỂM THỬ", 
               "So sánh sai số biên thời gian MAE, RMSE và độ nhạy theo môi trường tạp âm")

    # Bảng số liệu chuẩn xác từ simple_statistics.ipynb
    table_data = [
        ["Tên Tệp", "Môi Trường", "SNR (dB)", "MAE (ms)", "RMSE (ms)"],
        ["phone_F2", "Phone (Nữ)", "24.8 dB", "27.5000 ms", "37.1652 ms"],
        ["phone_M2", "Phone (Nam)", "27.0 dB", "2.5000 ms", "2.5000 ms"],
        ["studio_F2", "Studio (Nữ)", "49.3 dB", "5.0000 ms", "5.5929 ms"],
        ["studio_M2", "Studio (Nam)", "37.7 dB", "12.4940 ms", "16.0031 ms"],
        ["TB Phone (2 tệp)", "Điện thoại", "25.9 dB", "15.0000 ms", "19.8326 ms"],
        ["TB Studio (2 tệp)", "Phòng thu", "43.5 dB", "8.7470 ms", "10.7980 ms"],
        ["Toàn Bộ (4 tệp)", "Tổng thể", "34.7 dB", "11.8735 ms", "15.3153 ms"],
    ]

    # Matplotlib table bbox: [left, bottom, width, height] in normalized coordinates (0 to 1)
    # Canvas is 13.333 x 7.5
    # Table bounds: x: 0.7 -> 12.633 (w=11.933), y: 2.25 -> 5.95 (h=3.7)
    norm_left = 0.7 / 13.333
    norm_bottom = 2.25 / 7.5
    norm_width = 11.933 / 13.333
    norm_height = 3.7 / 7.5

    col_widths = [0.22, 0.18, 0.16, 0.22, 0.22]
    table = ax.table(cellText=table_data, colWidths=col_widths, loc="center",
                     bbox=[norm_left, norm_bottom, norm_width, norm_height])
    table.auto_set_font_size(False)

    # Style cells
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor(C_BORDER)
        cell.set_linewidth(1.0)
        
        if r == 0:
            cell.set_facecolor(C_SLATE_DARK)
            cell.get_text().set_color(C_WHITE)
            cell.get_text().set_fontweight("bold")
            cell.get_text().set_fontsize(13)
        elif r == 7:
            cell.set_facecolor(C_CYAN_DARK)
            cell.get_text().set_color(C_WHITE)
            cell.get_text().set_fontweight("bold")
            cell.get_text().set_fontsize(12.5)
        elif r in [5, 6]:
            cell.set_facecolor("#EFF6FF")
            cell.get_text().set_fontweight("bold")
            cell.get_text().set_color(C_ORANGE_DARK if r==5 else C_CYAN_DARK)
            cell.get_text().set_fontsize(12)
        else:
            cell.set_facecolor(C_WHITE if r%2==1 else C_CARD_BG)
            cell.get_text().set_color(C_SLATE_DARK)
            cell.get_text().set_fontsize(11.5)

    # Takeaway card (Below table)
    card = patches.FancyBboxPatch((0.7, 0.75), 11.933, 1.25, boxstyle="round,pad=0.06,rounding_size=0.1",
                                  facecolor=C_CARD_BG, edgecolor=C_BORDER, linewidth=1.2)
    ax.add_patch(card)
    ax.text(1.0, 1.60, "• Studio đạt độ chính xác vượt trội (MAE 8.7ms vs Phone 15.0ms) nhờ SNR cao (>37dB).", 
            fontsize=11.5, fontweight="bold", color=C_SLATE_DARK, va="center")
    ax.text(1.0, 1.25, "• Ngưỡng Bayes T* = 0.002495 phân tách ổn định, sai số toàn bộ trung bình đạt mức rất tốt (~11.9ms).", 
            fontsize=11.5, fontweight="bold", color=C_CYAN_DARK, va="center")
    ax.text(1.0, 0.90, "• Nhiễu nền kênh truyền điện thoại là tác nhân chính gây kéo dài khoảng lặng ở đuôi âm (phone_F2).", 
            fontsize=11.5, fontweight="bold", color=C_ORANGE_DARK, va="center")

    pdf.savefig(fig)
    plt.close()

# -------------------------------------------------------------
# SLIDE 5: DẠNG SÓNG & SAI SỐ ÂM HỌC
# -------------------------------------------------------------
def build_slide_5(pdf):
    fig, ax = create_slide_base(5)
    add_header(ax, "DẠNG SÓNG & PHÂN TÍCH NGUYÊN NHÂN SAI SỐ ÂM HỌC", 
               "So sánh trực quan biên chuẩn Ground-Truth vs Biên thuật toán và giải thích cơ chế âm học")

    # 4 Subplots in 2x2 grid
    # Top-Left: phone_F2
    p1 = MEDIA_DIR / "image19.png"
    if p1.exists():
        ax.imshow(mpimg.imread(str(p1)), extent=[0.7, 6.4, 3.8, 6.0], aspect="auto", zorder=2)
    
    b1 = patches.FancyBboxPatch((0.7, 3.32), 5.7, 0.38, boxstyle="round,pad=0.04,rounding_size=0.08",
                                facecolor=C_CARD_BG, edgecolor=C_BORDER, linewidth=1.0)
    ax.add_patch(b1)
    ax.text(3.55, 3.51, "• phone_F2: Nhiễu nền kéo dài đuôi → Err End 52.5ms (MAE 27.5ms)", 
            fontsize=10.5, fontweight="bold", color=C_ORANGE_DARK, ha="center", va="center")

    # Top-Right: phone_M2
    p2 = MEDIA_DIR / "image20.png"
    if p2.exists():
        ax.imshow(mpimg.imread(str(p2)), extent=[6.933, 12.633, 3.8, 6.0], aspect="auto", zorder=2)
    
    b2 = patches.FancyBboxPatch((6.933, 3.32), 5.7, 0.38, boxstyle="round,pad=0.04,rounding_size=0.08",
                                facecolor=C_CARD_BG, edgecolor=C_BORDER, linewidth=1.0)
    ax.add_patch(b2)
    ax.text(9.783, 3.51, "• phone_M2: Phân tách dứt khoát → Err Start=End 2.5ms (MAE 2.5ms)", 
            fontsize=10.5, fontweight="bold", color=C_CYAN_DARK, ha="center", va="center")

    # Bottom-Left: studio_F2
    p3 = MEDIA_DIR / "image21.png"
    if p3.exists():
        ax.imshow(mpimg.imread(str(p3)), extent=[0.7, 6.4, 1.15, 3.25], aspect="auto", zorder=2)
    
    b3 = patches.FancyBboxPatch((0.7, 0.68), 5.7, 0.38, boxstyle="round,pad=0.04,rounding_size=0.08",
                                facecolor=C_CARD_BG, edgecolor=C_BORDER, linewidth=1.0)
    ax.add_patch(b3)
    ax.text(3.55, 0.87, "• studio_F2: SNR cao 49dB, bám sát chuẩn → MAE 5.0ms (RMSE 5.6ms)", 
            fontsize=10.5, fontweight="bold", color=C_CYAN_DARK, ha="center", va="center")

    # Bottom-Right: studio_M2
    p4 = MEDIA_DIR / "image22.png"
    if p4.exists():
        ax.imshow(mpimg.imread(str(p4)), extent=[6.933, 12.633, 1.15, 3.25], aspect="auto", zorder=2)
    
    b4 = patches.FancyBboxPatch((6.933, 0.68), 5.7, 0.38, boxstyle="round,pad=0.04,rounding_size=0.08",
                                facecolor=C_CARD_BG, edgecolor=C_BORDER, linewidth=1.0)
    ax.add_patch(b4)
    ax.text(9.783, 0.87, "• studio_M2: Lặng giữa câu trễ bắt đầu → Err Start 22.5ms (MAE 12.5ms)", 
            fontsize=10.5, fontweight="bold", color=C_SLATE_DARK, ha="center", va="center")

    pdf.savefig(fig)
    plt.close()

def main():
    print(f"[*] Đang xuất file PDF trình chiếu -> {OUT_PDF}")
    with PdfPages(OUT_PDF) as pdf:
        build_slide_1(pdf)
        build_slide_2(pdf)
        build_slide_3(pdf)
        build_slide_4(pdf)
        build_slide_5(pdf)
    print(f"[+] Đã tạo PDF thành công ({OUT_PDF.stat().st_size / (1024*1024):.2f} MB)")

    # Cắt ảnh từng slide bằng pdftoppm
    import subprocess
    cmd = f'pdftoppm -jpeg -r 150 "{OUT_PDF}" "{OUT_IMG_DIR}/slide"'
    print(f"[*] Cắt ảnh các slide -> {cmd}")
    subprocess.run(cmd, shell=True, check=True)
    print("[+] Đã cắt ảnh hoàn tất!")

if __name__ == "__main__":
    main()
