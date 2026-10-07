#!/usr/bin/env python3
"""
scripts/export_presentation_pdf.py
Sinh trực tiếp file PDF trình chiếu presentation_speech_silence.pdf (16:9 Widescreen) 15 slides
chuẩn mỹ thuật Tech-HUD theo đúng template mẫu Digital vs. Analog...pdf
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg

# Palette chuẩn (Tech HUD)
C_WHITE = "#FFFFFF"
C_CARD_BG = "#F8FAFC"
C_CYAN = "#00A8FF"
C_CYAN_DARK = "#0284C7"
C_ORANGE = "#F58220"
C_ORANGE_DARK = "#C2410C"
C_SLATE_DARK = "#0F172A"
C_SLATE_MUTED = "#475569"
C_BORDER = "#CBD5E1"
C_HUD_DARK = "#1E293B"
C_GREEN = "#10B981"
C_RED = "#EF4444"

OUT_PDF = Path("presentation_speech_silence.pdf")
ASSETS_DIR = Path("assets/presentation")
TOTAL_SLIDES = 15

def create_slide_base(slide_num, total_slides=TOTAL_SLIDES):
    fig = plt.figure(figsize=(13.333, 7.5), facecolor=C_WHITE, dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.set_xlim(0, 13.333)
    ax.set_ylim(0, 7.5)

    # Top Orange Bar
    top_bar = patches.Rectangle((0, 7.35), 13.333, 0.15, facecolor=C_ORANGE, edgecolor="none")
    ax.add_patch(top_bar)

    # Bottom Dark Sub-bar
    bot_dark = patches.Rectangle((0, 0.18), 13.333, 0.05, facecolor=C_HUD_DARK, edgecolor="none")
    ax.add_patch(bot_dark)

    # Bottom Cyan Bar
    bot_bar = patches.Rectangle((0, 0), 13.333, 0.18, facecolor=C_CYAN, edgecolor="none")
    ax.add_patch(bot_bar)

    # Footer Text
    footer_text = f"BÁO CÁO THI GIỮA KỲ — MÔN XỬ LÝ TÍN HIỆU SỐ  |  SLIDE {slide_num}/{total_slides}"
    ax.text(12.6, 0.32, footer_text, fontsize=9.5, color=C_SLATE_MUTED, ha="right", va="center", fontweight="medium")

    return fig, ax

def add_header(ax, title, subtitle=None):
    ax.text(0.7, 6.75, title.upper(), fontsize=22, fontweight="bold", color=C_CYAN, va="center")
    if subtitle:
        ax.text(0.7, 6.32, subtitle, fontsize=13, fontweight="bold", color=C_SLATE_MUTED, va="center")

def build_slide_1(pdf):
    fig, ax = create_slide_base(1)

    hud_box = patches.FancyBboxPatch((0.8, 0.7), 11.733, 6.1, boxstyle="round,pad=0.1,rounding_size=0.2",
                                     facecolor=C_WHITE, edgecolor=C_HUD_DARK, linewidth=2.5)
    ax.add_patch(hud_box)

    badge = patches.FancyBboxPatch((1.3, 5.85), 4.8, 0.52, boxstyle="round,pad=0.05,rounding_size=0.1",
                                   facecolor=C_ORANGE, edgecolor="none")
    ax.add_patch(badge)
    ax.text(3.7, 6.11, "XỬ LÝ TÍN HIỆU SỐ — ĐỒ ÁN GIỮA KỲ", fontsize=12.5, fontweight="bold", color=C_WHITE, ha="center", va="center")

    ax.text(1.3, 4.8, "PHÂN ĐOẠN TIẾNG NÓI\nVÀ KHOẢNG LẶNG", fontsize=34, fontweight="bold", color=C_CYAN, va="center", linespacing=1.2)
    ax.text(1.3, 3.65, "Khảo sát & Đánh giá Thực nghiệm 03 Thuật toán Phân đoạn trên Tín hiệu Thực tế", fontsize=15.5, fontweight="bold", color=C_SLATE_DARK, va="center")

    card = patches.FancyBboxPatch((1.3, 1.15), 10.7, 2.1, boxstyle="round,pad=0.08,rounding_size=0.12",
                                  facecolor=C_CARD_BG, edgecolor=C_BORDER, linewidth=1.2)
    ax.add_patch(card)

    details = (
        "• Nhóm Sinh viên Thực hiện:  Báo cáo thi giữa kỳ môn Xử lý tín hiệu số (3 phút slide + 1 phút demo)\n\n"
        "• 03 Thuật toán Phân đoạn:  Tìm kiếm Nhị phân (Hodgkinson), Histogram (Giannakopoulos), Gaussian Bayes\n\n"
        "• Tập Dữ liệu Thực nghiệm:  04 file Huấn luyện (tìm ngưỡng tối ưu) & 04 file Kiểm thử (đánh giá định lượng MAE/RMSE)"
    )
    ax.text(1.6, 2.2, details, fontsize=13, color=C_SLATE_DARK, va="center", linespacing=1.35)

    pdf.savefig(fig)
    plt.close()

def build_slide_2(pdf):
    fig, ax = create_slide_base(2)
    add_header(ax, "1. TỔNG QUAN BÀI TOÁN & THÁCH THỨC", "Đặc tính Tín hiệu Tiếng nói và Yêu cầu Tách Biên Thời gian")

    # Left card: Mục tiêu
    c_left = patches.FancyBboxPatch((0.7, 0.8), 5.7, 5.2, boxstyle="round,pad=0.08,rounding_size=0.12",
                                    facecolor=C_CARD_BG, edgecolor=C_CYAN, linewidth=1.8)
    ax.add_patch(c_left)
    ax.text(1.0, 5.5, "MỤC TIÊU PHÂN ĐOẠN (VAD)", fontsize=15, fontweight="bold", color=C_CYAN_DARK)
    txt_l = (
        "• Định vị ranh giới thời gian chính xác\n\n"
        "• Phân tách Speech vs Silence trong file audio\n\n"
        "• Giảm thiểu sai số MAE & RMSE < 25 ms\n\n"
        "• Bước tiền xử lý cốt lõi cho ASR & Nhận dạng"
    )
    ax.text(1.0, 3.2, txt_l, fontsize=13, color=C_SLATE_DARK, va="center", linespacing=1.5)

    # Right card: Thách thức
    c_right = patches.FancyBboxPatch((6.9, 0.8), 5.7, 5.2, boxstyle="round,pad=0.08,rounding_size=0.12",
                                     facecolor=C_CARD_BG, edgecolor=C_ORANGE, linewidth=1.8)
    ax.add_patch(c_right)
    ax.text(7.2, 5.5, "THÁCH THỨC MÔI TRƯỜNG THỰC TẾ", fontsize=15, fontweight="bold", color=C_ORANGE_DARK)
    txt_r = (
        "• Nhiễu nền điện thoại (SNR thấp 24-27 dB)\n\n"
        "• Âm vô thanh (/s/, /t/, /f/) năng lượng rất thấp\n\n"
        "• Dễ nhầm phụ âm yếu thành khoảng lặng\n\n"
        "• Ngưỡng đơn toàn cục cần độ thích nghi cao"
    )
    ax.text(7.2, 3.2, txt_r, fontsize=13, color=C_SLATE_DARK, va="center", linespacing=1.5)

    pdf.savefig(fig)
    plt.close()

def build_slide_3(pdf):
    fig, ax = create_slide_base(3)
    add_header(ax, "2. QUY TRÌNH XỬ LÝ TÍN HIỆU 5 BƯỚC", "Kiến trúc Pipeline Chuẩn hóa từ Dạng sóng đến Biên phân đoạn")

    img_path = ASSETS_DIR / "fig_pipeline.png"
    if img_path.exists():
        img = mpimg.imread(str(img_path))
        ax.imshow(img, extent=[0.7, 8.2, 0.8, 5.9], aspect="auto", zorder=2)

    card = patches.FancyBboxPatch((8.5, 0.8), 4.133, 5.2, boxstyle="round,pad=0.08,rounding_size=0.12",
                                  facecolor=C_CARD_BG, edgecolor=C_BORDER, linewidth=1.2)
    ax.add_patch(card)
    ax.text(8.8, 5.5, "CHI TIẾT THAM SỐ", fontsize=15, fontweight="bold", color=C_ORANGE)
    txt = (
        "1. Chuẩn hóa:\n   Scale biên độ [-1, 1]\n\n"
        "2. Cửa sổ:\n   Hamming 20ms, nhảy 10ms\n\n"
        "3. Đặc trưng:\n   STE & log(STE)\n\n"
        "4. Phân ngưỡng:\n   Toàn cục (Global Threshold)\n\n"
        "5. Hậu xử lý:\n   Lọc nhiễu đoạn < 200ms"
    )
    ax.text(8.8, 3.0, txt, fontsize=12.5, color=C_SLATE_DARK, va="center", linespacing=1.25)

    pdf.savefig(fig)
    plt.close()

def build_slide_4(pdf):
    fig, ax = create_slide_base(4)
    add_header(ax, "3. ĐẶC TRƯNG NĂNG LƯỢNG: STE VS LOG(STE)", "So sánh Không gian Biểu diễn Tuyến tính và Phi tuyến")

    img_path = ASSETS_DIR / "fig_ste_vs_logste.png"
    if img_path.exists():
        img = mpimg.imread(str(img_path))
        ax.imshow(img, extent=[0.7, 8.8, 0.8, 5.9], aspect="auto", zorder=2)

    card = patches.FancyBboxPatch((9.1, 0.8), 3.533, 5.2, boxstyle="round,pad=0.08,rounding_size=0.12",
                                  facecolor=C_CARD_BG, edgecolor=C_BORDER, linewidth=1.2)
    ax.add_patch(card)
    ax.text(9.3, 5.5, "ƯU THẾ CỦA LOG(STE)", fontsize=14, fontweight="bold", color=C_ORANGE)
    txt = (
        "• STE tuyến tính:\n"
        "  Dải động lệch mạnh về 0.\n\n"
        "• log(STE) phi tuyến:\n"
        "  Kéo dãn phân bố im lặng.\n\n"
        "• Tách rõ 2 đỉnh:\n"
        "  Tạo thung lũng rõ ràng\n"
        "  để đặt ngưỡng tối ưu."
    )
    ax.text(9.3, 3.2, txt, fontsize=12.5, color=C_SLATE_DARK, va="center", linespacing=1.4)

    pdf.savefig(fig)
    plt.close()

def build_slide_5(pdf):
    fig, ax = create_slide_base(5)
    add_header(ax, "4. THUẬT TOÁN 1: TÌM KIẾM NHỊ PHÂN (TT1)", "Tối ưu hóa Sai số Biên thời gian bằng Phân đôi Không gian Ngưỡng")

    img_path = ASSETS_DIR / "fig_tt1_binary_flow.png"
    if img_path.exists():
        img = mpimg.imread(str(img_path))
        ax.imshow(img, extent=[0.7, 8.2, 0.8, 5.9], aspect="auto", zorder=2)

    card = patches.FancyBboxPatch((8.5, 0.8), 4.133, 5.2, boxstyle="round,pad=0.08,rounding_size=0.12",
                                  facecolor=C_CARD_BG, edgecolor=C_CYAN, linewidth=1.8)
    ax.add_patch(card)
    ax.text(8.8, 5.5, "KẾT QUẢ HUẤN LUYỆN", fontsize=15, fontweight="bold", color=C_CYAN_DARK)
    txt = (
        "• Khoảng tìm kiếm: [0.0, 1.0]\n\n"
        "• Số vòng lặp: 12 bước\n\n"
        "• Độ mịn ngưỡng: 1/2^12 ≈ 0.00024\n\n"
        "• Ngưỡng tối ưu: T = 0.000798\n\n"
        "• Hàm mất mát: Tổng sai số khung nhỏ nhất"
    )
    ax.text(8.8, 3.2, txt, fontsize=12.5, color=C_SLATE_DARK, va="center", linespacing=1.4)

    pdf.savefig(fig)
    plt.close()

def build_slide_6(pdf):
    fig, ax = create_slide_base(6)
    add_header(ax, "5. THUẬT TOÁN 2: PHÂN TÍCH HISTOGRAM (TT2)", "Xác định Đáy Thung lũng giữa 2 Đỉnh Cực đại Năng lượng Phi tuyến")

    img_path = ASSETS_DIR / "fig_tt2_histogram_flow.png"
    if img_path.exists():
        img = mpimg.imread(str(img_path))
        ax.imshow(img, extent=[0.7, 8.2, 0.8, 5.9], aspect="auto", zorder=2)

    card = patches.FancyBboxPatch((8.5, 0.8), 4.133, 5.2, boxstyle="round,pad=0.08,rounding_size=0.12",
                                  facecolor=C_CARD_BG, edgecolor=C_ORANGE, linewidth=1.8)
    ax.add_patch(card)
    ax.text(8.8, 5.5, "KẾT QUẢ HUẤN LUYỆN", fontsize=15, fontweight="bold", color=C_ORANGE_DARK)
    txt = (
        "• Không gian: log(STE)\n\n"
        "• Số bins: Histogram đa mức\n\n"
        "• Trọng số lệch: W = 2.0 (nghiêng về silence)\n\n"
        "• Ngưỡng tối ưu: T = -2.4375\n\n"
        "• Kháng nhiễu: Tối ưu nhất cho môi trường Phone"
    )
    ax.text(8.8, 3.2, txt, fontsize=12.5, color=C_SLATE_DARK, va="center", linespacing=1.4)

    pdf.savefig(fig)
    plt.close()

def build_slide_7(pdf):
    fig, ax = create_slide_base(7)
    add_header(ax, "6. THUẬT TOÁN 3: PHÂN PHỐI GAUSS BAYES (TT3)", "Phân loại Thống kê Mô hình hóa Hàm Mật độ Xác suất (PDF)")

    img_path = ASSETS_DIR / "fig_tt3_gaussian_flow.png"
    if img_path.exists():
        img = mpimg.imread(str(img_path))
        ax.imshow(img, extent=[0.7, 8.2, 0.8, 5.9], aspect="auto", zorder=2)

    card = patches.FancyBboxPatch((8.5, 0.8), 4.133, 5.2, boxstyle="round,pad=0.08,rounding_size=0.12",
                                  facecolor=C_CARD_BG, edgecolor=C_GREEN, linewidth=1.8)
    ax.add_patch(card)
    ax.text(8.8, 5.5, "KẾT QUẢ HUẤN LUYỆN", fontsize=15, fontweight="bold", color=C_GREEN)
    txt = (
        "• Silence: mu=0.00025, sigma=0.00063\n\n"
        "• Speech: mu=0.20247, sigma=0.23569\n\n"
        "• Chuẩn Bayes: Điểm giao xác suất 2 lớp\n\n"
        "• Ngưỡng tối ưu: T = 0.000792\n\n"
        "• Tương đồng TT1: Hội tụ về cùng mức năng lượng"
    )
    ax.text(8.8, 3.2, txt, fontsize=12.5, color=C_SLATE_DARK, va="center", linespacing=1.4)

    pdf.savefig(fig)
    plt.close()

def build_slide_8(pdf):
    fig, ax = create_slide_base(8)
    add_header(ax, "7. TỔNG HỢP NGƯỠNG TRÊN TẬP HUẤN LUYỆN", "So sánh Cơ chế Hội tụ và Ngưỡng Toàn cục của 03 Thuật toán")

    img_path = ASSETS_DIR / "fig_training_summary.png"
    if img_path.exists():
        img = mpimg.imread(str(img_path))
        ax.imshow(img, extent=[0.7, 12.633, 0.8, 5.9], aspect="auto", zorder=2)

    pdf.savefig(fig)
    plt.close()

def build_slide_9(pdf):
    fig, ax = create_slide_base(9)
    add_header(ax, "8. KẾT QUẢ THỰC NGHIỆM TT1: BINARY SEARCH", "Đánh giá trên 04 File Kiểm thử — Ngưỡng Toàn cục T = 0.000798")

    img_path = ASSETS_DIR / "fig_test_binary_4files.png"
    if img_path.exists():
        img = mpimg.imread(str(img_path))
        ax.imshow(img, extent=[0.7, 12.633, 0.8, 5.9], aspect="auto", zorder=2)

    pdf.savefig(fig)
    plt.close()

def build_slide_10(pdf):
    fig, ax = create_slide_base(10)
    add_header(ax, "9. KẾT QUẢ THỰC NGHIỆM TT2: HISTOGRAM LOG(STE)", "Đánh giá trên 04 File Kiểm thử — Ngưỡng Toàn cục T = -2.4375 (W=2.0)")

    img_path = ASSETS_DIR / "fig_test_histogram_4files.png"
    if img_path.exists():
        img = mpimg.imread(str(img_path))
        ax.imshow(img, extent=[0.7, 12.633, 0.8, 5.9], aspect="auto", zorder=2)

    pdf.savefig(fig)
    plt.close()

def build_slide_11(pdf):
    fig, ax = create_slide_base(11)
    add_header(ax, "10. KẾT QUẢ THỰC NGHIỆM TT3: GAUSSIAN BAYES", "Đánh giá trên 04 File Kiểm thử — Ngưỡng Toàn cục T = 0.000792")

    img_path = ASSETS_DIR / "fig_test_gaussian_4files.png"
    if img_path.exists():
        img = mpimg.imread(str(img_path))
        ax.imshow(img, extent=[0.7, 12.633, 0.8, 5.9], aspect="auto", zorder=2)

    pdf.savefig(fig)
    plt.close()

def build_slide_12(pdf):
    fig, ax = create_slide_base(12)
    add_header(ax, "11. ĐÁNH GIÁ MÔI TRƯỜNG PHÒNG THU (STUDIO)", "Tín hiệu Tinh sạch High SNR (37.7 - 49.3 dB) — Độ chính xác Tuyệt đối")

    img_path = ASSETS_DIR / "fig_studio_deepdive.png"
    if img_path.exists():
        img = mpimg.imread(str(img_path))
        ax.imshow(img, extent=[0.7, 9.0, 0.8, 5.9], aspect="auto", zorder=2)

    card = patches.FancyBboxPatch((9.3, 0.8), 3.333, 5.2, boxstyle="round,pad=0.08,rounding_size=0.12",
                                  facecolor=C_CARD_BG, edgecolor=C_CYAN, linewidth=1.8)
    ax.add_patch(card)
    ax.text(9.5, 5.5, "ĐẶC TÍNH STUDIO", fontsize=15, fontweight="bold", color=C_CYAN_DARK)
    txt = (
        "• SNR cực cao:\n"
        "  Studio F2: 49.3 dB\n"
        "  Studio M2: 37.7 dB\n\n"
        "• Sai số cực thấp:\n"
        "  MAE từ 2.49 đến 12.49 ms\n\n"
        "• Kết luận:\n"
        "  Cả 3 thuật toán đều phân\n"
        "  đoạn gần như hoàn hảo."
    )
    ax.text(9.5, 3.2, txt, fontsize=12.5, color=C_SLATE_DARK, va="center", linespacing=1.4)

    pdf.savefig(fig)
    plt.close()

def build_slide_13(pdf):
    fig, ax = create_slide_base(13)
    add_header(ax, "12. ĐÁNH GIÁ MÔI TRƯỜNG ĐIỆN THOẠI (PHONE)", "Tín hiệu Nhiễu nền Low SNR (24.8 - 27.0 dB) — Ưu thế Kháng nhiễu")

    img_path = ASSETS_DIR / "fig_phone_deepdive.png"
    if img_path.exists():
        img = mpimg.imread(str(img_path))
        ax.imshow(img, extent=[0.7, 9.0, 0.8, 5.9], aspect="auto", zorder=2)

    card = patches.FancyBboxPatch((9.3, 0.8), 3.333, 5.2, boxstyle="round,pad=0.08,rounding_size=0.12",
                                  facecolor=C_CARD_BG, edgecolor=C_ORANGE, linewidth=1.8)
    ax.add_patch(card)
    ax.text(9.5, 5.5, "TÁC ĐỘNG CỦA NHIỄU", fontsize=15, fontweight="bold", color=C_ORANGE_DARK)
    txt = (
        "• SNR thấp:\n"
        "  Phone M2: 27.0 dB\n"
        "  Phone F2: 24.8 dB\n\n"
        "• TT2 vượt trội:\n"
        "  MAE chỉ 27.5 ms (so với\n"
        "  35.0 ms của TT1/TT3)\n\n"
        "• Lý do:\n"
        "  log(STE) nén nhiễu nền tốt."
    )
    ax.text(9.5, 3.2, txt, fontsize=12.5, color=C_SLATE_DARK, va="center", linespacing=1.4)

    pdf.savefig(fig)
    plt.close()

def build_slide_14(pdf):
    fig, ax = create_slide_base(14)
    add_header(ax, "13. TỔNG HỢP ĐỊNH LƯỢNG & TÁC ĐỘNG CỦA SNR", "Đối chiếu Sai số MAE/RMSE giữa 03 Thuật toán trên Toàn bộ Tập Kiểm thử")

    img_path = ASSETS_DIR / "fig_snr_comparison.png"
    if img_path.exists():
        img = mpimg.imread(str(img_path))
        ax.imshow(img, extent=[0.7, 8.2, 0.8, 5.9], aspect="auto", zorder=2)

    card = patches.FancyBboxPatch((8.5, 0.8), 4.133, 5.2, boxstyle="round,pad=0.08,rounding_size=0.12",
                                  facecolor=C_CARD_BG, edgecolor=C_BORDER, linewidth=1.2)
    ax.add_patch(card)
    ax.text(8.8, 5.5, "BẢNG SAI SỐ TRUNG BÌNH", fontsize=15, fontweight="bold", color=C_ORANGE)
    txt = (
        "• Môi trường Studio:\n"
        "  TT1: 7.49 ms | TT2: 8.75 ms\n\n"
        "• Môi trường Phone:\n"
        "  TT1: 35.0 ms | TT2: 27.5 ms\n\n"
        "• Toàn bộ 04 file:\n"
        "  TT1: 21.25 ms\n"
        "  TT2: 18.12 ms (Tốt nhất)\n"
        "  TT3: 21.25 ms"
    )
    ax.text(8.8, 3.2, txt, fontsize=12.5, color=C_SLATE_DARK, va="center", linespacing=1.4)

    pdf.savefig(fig)
    plt.close()

def build_slide_15(pdf):
    fig, ax = create_slide_base(15)
    add_header(ax, "14. KẾT LUẬN & HƯỚNG MỞ RỘNG NGƯỠNG KÉP", "Giải pháp Khắc phục Âm Vô thanh bằng Zero Crossing Rate (ZCR)")

    img_path = ASSETS_DIR / "fig_zcr_concept.png"
    if img_path.exists():
        img = mpimg.imread(str(img_path))
        ax.imshow(img, extent=[0.7, 12.633, 0.8, 5.9], aspect="auto", zorder=2)

    pdf.savefig(fig)
    plt.close()

def main():
    print(f"=== Đang xuất file PDF trình chiếu: {OUT_PDF} ===")
    with PdfPages(OUT_PDF) as pdf:
        build_slide_1(pdf)
        build_slide_2(pdf)
        build_slide_3(pdf)
        build_slide_4(pdf)
        build_slide_5(pdf)
        build_slide_6(pdf)
        build_slide_7(pdf)
        build_slide_8(pdf)
        build_slide_9(pdf)
        build_slide_10(pdf)
        build_slide_11(pdf)
        build_slide_12(pdf)
        build_slide_13(pdf)
        build_slide_14(pdf)
        build_slide_15(pdf)
    print(f"=== ĐÃ XUẤT THÀNH CÔNG 15 SLIDES VÀO: {OUT_PDF} ===")

if __name__ == "__main__":
    main()
