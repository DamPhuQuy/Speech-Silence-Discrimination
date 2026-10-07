const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");

console.log("=== Bắt đầu khởi tạo Presentation Deck 15 Slide bằng pptxgenjs ===");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10.0" x 5.625"
pres.title = "Phân đoạn Tiếng nói và Khoảng lặng (15 Slides)";
pres.subject = "Báo cáo Giữa kỳ môn Xử lý Tín hiệu Số - XLTHS 2026";
pres.author = "Nhóm Sinh viên";

// Bảng màu chuẩn từ template (KHÔNG CÓ DẤU #)
const COLOR = {
  BG_WHITE: "FFFFFF",
  BG_CARD: "F8FAFC",
  CYAN_ACCENT: "00A8FF",
  CYAN_DARK: "0284C7",
  ORANGE_ACCENT: "F58220",
  ORANGE_DARK: "C2410C",
  SLATE_DARK: "0F172A",
  SLATE_MUTED: "475569",
  BORDER_CARD: "CBD5E1",
  HUD_DARK: "1E293B",
  GREEN_ACCENT: "10B981",
  RED_ACCENT: "EF4444"
};

const FONT_PRIMARY = "Arial";
const TOTAL_SLIDES = 15;

// Helper: Vẽ thanh HUD header & footer theo ngôn ngữ thiết kế của template
function applySlideChrome(slide, slideNumber, totalSlides = TOTAL_SLIDES) {
  // Top Orange Accent Stripe
  slide.addShape(pres.ShapeType.rect, {
    x: 0,
    y: 0,
    w: 10.0,
    h: 0.12,
    fill: { color: COLOR.ORANGE_ACCENT },
    line: { color: COLOR.ORANGE_ACCENT }
  });

  // Bottom Cyan Accent Stripe
  slide.addShape(pres.ShapeType.rect, {
    x: 0,
    y: 5.5,
    w: 10.0,
    h: 0.125,
    fill: { color: COLOR.CYAN_ACCENT },
    line: { color: COLOR.CYAN_ACCENT }
  });

  // Bottom Sub-line Dark
  slide.addShape(pres.ShapeType.rect, {
    x: 0,
    y: 5.46,
    w: 10.0,
    h: 0.04,
    fill: { color: COLOR.HUD_DARK },
    line: { color: COLOR.HUD_DARK }
  });

  // Footer slide number & metadata
  slide.addText(`BÁO CÁO THI GIỮA KỲ — MÔN XỬ LÝ TÍN HIỆU SỐ | SLIDE ${slideNumber}/${totalSlides}`, {
    x: 0.5,
    y: 5.25,
    w: 9.0,
    h: 0.22,
    fontSize: 9,
    fontFace: FONT_PRIMARY,
    color: COLOR.SLATE_MUTED,
    align: "right",
    margin: 0
  });
}

// Helper: Header của các slide nội dung
function addSlideHeader(slide, titleText, subtitleText) {
  slide.addText(titleText.toUpperCase(), {
    x: 0.5,
    y: 0.25,
    w: 9.0,
    h: 0.45,
    fontSize: 22,
    fontFace: FONT_PRIMARY,
    bold: true,
    color: COLOR.CYAN_ACCENT,
    margin: 0
  });

  if (subtitleText) {
    slide.addText(subtitleText, {
      x: 0.5,
      y: 0.68,
      w: 9.0,
      h: 0.3,
      fontSize: 14,
      fontFace: FONT_PRIMARY,
      bold: true,
      color: COLOR.SLATE_MUTED,
      margin: 0
    });
  }
}

// -------------------------------------------------------------
// SLIDE 1: COVER
// -------------------------------------------------------------
{
  const slide = pres.addSlide();
  applySlideChrome(slide, 1);

  // Outer Tech HUD Border Frame
  slide.addShape(pres.ShapeType.roundRect, {
    x: 0.6,
    y: 0.5,
    w: 8.8,
    h: 4.6,
    rectRadius: 0.15,
    fill: { color: COLOR.BG_WHITE },
    line: { color: COLOR.HUD_DARK, width: 2.0 }
  });

  // Category Tag Badge
  slide.addShape(pres.ShapeType.roundRect, {
    x: 1.0,
    y: 0.8,
    w: 3.8,
    h: 0.4,
    rectRadius: 0.08,
    fill: { color: COLOR.ORANGE_ACCENT },
    line: { color: COLOR.ORANGE_ACCENT }
  });
  slide.addText("XỬ LÝ TÍN HIỆU SỐ — ĐỒ ÁN GIỮA KỲ", {
    x: 1.0,
    y: 0.8,
    w: 3.8,
    h: 0.4,
    fontSize: 12,
    fontFace: FONT_PRIMARY,
    bold: true,
    color: COLOR.BG_WHITE,
    align: "center",
    valign: "middle",
    margin: 0
  });

  // Main Title
  slide.addText("PHÂN ĐOẠN TIẾNG NÓI\nVÀ KHOẢNG LẶNG", {
    x: 1.0,
    y: 1.35,
    w: 8.0,
    h: 1.2,
    fontSize: 32,
    fontFace: FONT_PRIMARY,
    bold: true,
    color: COLOR.CYAN_ACCENT,
    lineSpacing: 36,
    margin: 0
  });

  // Subtitle
  slide.addText("Khảo sát & Đánh giá Thực nghiệm 03 Thuật toán Phân đoạn trên Tín hiệu Thực tế", {
    x: 1.0,
    y: 2.65,
    w: 8.0,
    h: 0.35,
    fontSize: 15,
    fontFace: FONT_PRIMARY,
    bold: true,
    color: COLOR.SLATE_DARK,
    margin: 0
  });

  // Details Card Box
  slide.addShape(pres.ShapeType.roundRect, {
    x: 1.0,
    y: 3.15,
    w: 8.0,
    h: 1.6,
    rectRadius: 0.1,
    fill: { color: COLOR.BG_CARD },
    line: { color: COLOR.BORDER_CARD, width: 1.0 }
  });

  slide.addText([
    { text: "• Nhóm Sinh viên: ", options: { bold: true, color: COLOR.ORANGE_DARK, fontSize: 13 } },
    { text: "Báo cáo thực nghiệm chuyên sâu (3 phút slide + 1 phút demo)\n", options: { color: COLOR.SLATE_DARK, fontSize: 13 } },
    { text: "• 03 Thuật toán: ", options: { bold: true, color: COLOR.CYAN_DARK, fontSize: 13 } },
    { text: "Tìm kiếm Nhị phân (Hodgkinson), Histogram (Giannakopoulos), Gaussian Bayes\n", options: { color: COLOR.SLATE_DARK, fontSize: 13 } },
    { text: "• Dữ liệu kiểm thử: ", options: { bold: true, color: COLOR.GREEN_ACCENT, fontSize: 13 } },
    { text: "04 file WAV (phone_F2, phone_M2, studio_F2, studio_M2) & nhãn .lab", options: { color: COLOR.SLATE_DARK, fontSize: 13 } }
  ], {
    x: 1.2,
    y: 3.25,
    w: 7.6,
    h: 1.4,
    fontFace: FONT_PRIMARY,
    lineSpacing: 22,
    margin: 0
  });

  slide.addNotes("Kính thưa Thầy và các bạn, hôm nay nhóm xin báo cáo đề tài Phân đoạn tiếng nói và khoảng lặng trên tín hiệu âm thanh sử dụng 3 thuật toán xác định ngưỡng toàn cục.");
}

// -------------------------------------------------------------
// SLIDE 2: TỔNG QUAN BÀI TOÁN & THÁCH THỨC
// -------------------------------------------------------------
{
  const slide = pres.addSlide();
  applySlideChrome(slide, 2);
  addSlideHeader(slide, "1. TỔNG QUAN BÀI TOÁN & THÁCH THỨC", "Đặc tính Tín hiệu Tiếng nói và Yêu cầu Tách Biên Thời gian");

  // Left Card: Mục tiêu bài toán
  slide.addShape(pres.ShapeType.roundRect, {
    x: 0.5,
    y: 1.1,
    w: 4.3,
    h: 3.9,
    rectRadius: 0.1,
    fill: { color: COLOR.BG_CARD },
    line: { color: COLOR.CYAN_ACCENT, width: 1.5 }
  });
  slide.addText("MỤC TIÊU PHÂN ĐOẠN (VAD)", {
    x: 0.7,
    y: 1.25,
    w: 3.9,
    h: 0.35,
    fontSize: 16,
    fontFace: FONT_PRIMARY,
    bold: true,
    color: COLOR.CYAN_DARK
  });
  slide.addText([
    { text: "• Định vị ranh giới thời gian chính xác\n\n", options: { bold: true, color: COLOR.SLATE_DARK } },
    { text: "• Phân tách Speech vs Silence trong file audio\n\n", options: { color: COLOR.SLATE_DARK } },
    { text: "• Giảm thiểu sai số MAE & RMSE < 25 ms\n\n", options: { bold: true, color: COLOR.GREEN_ACCENT } },
    { text: "• Bước tiền xử lý cốt lõi cho ASR & Nhận dạng", options: { color: COLOR.SLATE_MUTED } }
  ], {
    x: 0.7,
    y: 1.75,
    w: 3.9,
    h: 3.0,
    fontSize: 18,
    fontFace: FONT_PRIMARY,
    margin: 0
  });

  // Right Card: Thách thức kỹ thuật
  slide.addShape(pres.ShapeType.roundRect, {
    x: 5.1,
    y: 1.1,
    w: 4.4,
    h: 3.9,
    rectRadius: 0.1,
    fill: { color: COLOR.BG_CARD },
    line: { color: COLOR.ORANGE_ACCENT, width: 1.5 }
  });
  slide.addText("THÁCH THỨC MÔI TRƯỜNG THỰC TẾ", {
    x: 5.3,
    y: 1.25,
    w: 4.0,
    h: 0.35,
    fontSize: 16,
    fontFace: FONT_PRIMARY,
    bold: true,
    color: COLOR.ORANGE_DARK
  });
  slide.addText([
    { text: "• Nhiễu nền điện thoại (SNR thấp 24-27 dB)\n\n", options: { bold: true, color: COLOR.ORANGE_DARK } },
    { text: "• Âm vô thanh (/s/, /t/, /f/) năng lượng rất thấp\n\n", options: { bold: true, color: COLOR.RED_ACCENT } },
    { text: "• Dễ nhầm phụ âm yếu thành khoảng lặng\n\n", options: { color: COLOR.SLATE_DARK } },
    { text: "• Ngưỡng đơn toàn cục cần độ thích nghi cao", options: { bold: true, color: COLOR.CYAN_DARK } }
  ], {
    x: 5.3,
    y: 1.75,
    w: 4.0,
    h: 3.0,
    fontSize: 18,
    fontFace: FONT_PRIMARY,
    margin: 0
  });

  slide.addNotes("Bài toán phân đoạn tiếng nói đối mặt với 2 thách thức lớn: nhiễu môi trường trong các cuộc gọi điện thoại và sự tồn tại của các phụ âm vô thanh mang năng lượng rất thấp.");
}

// -------------------------------------------------------------
// SLIDE 3: PIPELINE XỬ LÝ 5 BƯỚC
// -------------------------------------------------------------
{
  const slide = pres.addSlide();
  applySlideChrome(slide, 3);
  addSlideHeader(slide, "2. QUY TRÌNH XỬ LÝ TÍN HIỆU 5 BƯỚC", "Kiến trúc Pipeline Chuẩn hóa từ Dạng sóng đến Biên phân đoạn");

  // Image Left
  const imgPath = path.join(__dirname, "../assets/presentation/fig_pipeline.png");
  if (fs.existsSync(imgPath)) {
    slide.addImage({
      path: imgPath,
      x: 0.5,
      y: 1.1,
      w: 5.3,
      h: 3.9
    });
  }

  // Right Column: Summary Card
  slide.addShape(pres.ShapeType.roundRect, {
    x: 6.0,
    y: 1.1,
    w: 3.5,
    h: 3.9,
    rectRadius: 0.1,
    fill: { color: COLOR.BG_CARD },
    line: { color: COLOR.BORDER_CARD, width: 1.0 }
  });

  slide.addText("CHI TIẾT THAM SỐ", {
    x: 6.2,
    y: 1.25,
    w: 3.1,
    h: 0.35,
    fontSize: 16,
    fontFace: FONT_PRIMARY,
    bold: true,
    color: COLOR.ORANGE_ACCENT
  });

  slide.addText([
    { text: "1. Chuẩn hóa: ", options: { bold: true, color: COLOR.CYAN_DARK } },
    { text: "Scale biên độ [-1, 1]\n", options: { color: COLOR.SLATE_DARK } },
    { text: "2. Cửa sổ: ", options: { bold: true, color: COLOR.CYAN_DARK } },
    { text: "Hamming 20ms, nhảy 10ms\n", options: { color: COLOR.SLATE_DARK } },
    { text: "3. Đặc trưng: ", options: { bold: true, color: COLOR.CYAN_DARK } },
    { text: "STE & log(STE)\n", options: { color: COLOR.SLATE_DARK } },
    { text: "4. Phân ngưỡng: ", options: { bold: true, color: COLOR.CYAN_DARK } },
    { text: "Toàn cục (Global Threshold)\n", options: { color: COLOR.SLATE_DARK } },
    { text: "5. Hậu xử lý: ", options: { bold: true, color: COLOR.CYAN_DARK } },
    { text: "Lọc nhiễu đoạn < 200ms", options: { color: COLOR.SLATE_DARK } }
  ], {
    x: 6.2,
    y: 1.75,
    w: 3.1,
    h: 3.0,
    fontSize: 18,
    fontFace: FONT_PRIMARY,
    lineSpacing: 24,
    margin: 0
  });

  slide.addNotes("Pipeline gồm 5 bước khép kín: Chuẩn hóa biên độ; Phân khung Hamming 20ms chồng chập 10ms; Trích xuất STE/log(STE); Áp ngưỡng toàn cục; và Hậu xử lý lọc các đoạn dưới 200ms.");
}

// -------------------------------------------------------------
// SLIDE 4: ĐẶC TRƯNG STE VS LOG(STE)
// -------------------------------------------------------------
{
  const slide = pres.addSlide();
  applySlideChrome(slide, 4);
  addSlideHeader(slide, "3. ĐẶC TRƯNG NĂNG LƯỢNG: STE VS LOG(STE)", "So sánh Không gian Biểu diễn Tuyến tính và Phi tuyến");

  const imgPath = path.join(__dirname, "../assets/presentation/fig_ste_vs_logste.png");
  if (fs.existsSync(imgPath)) {
    slide.addImage({
      path: imgPath,
      x: 0.5,
      y: 1.1,
      w: 6.0,
      h: 3.9
    });
  }

  // Right card
  slide.addShape(pres.ShapeType.roundRect, {
    x: 6.7,
    y: 1.1,
    w: 2.8,
    h: 3.9,
    rectRadius: 0.1,
    fill: { color: COLOR.BG_CARD },
    line: { color: COLOR.BORDER_CARD, width: 1.0 }
  });

  slide.addText("ƯU THẾ CỦA LOG(STE)", {
    x: 6.85,
    y: 1.25,
    w: 2.5,
    h: 0.35,
    fontSize: 15,
    fontFace: FONT_PRIMARY,
    bold: true,
    color: COLOR.ORANGE_ACCENT
  });

  slide.addText([
    { text: "• STE tuyến tính:\n", options: { bold: true, color: COLOR.CYAN_DARK } },
    { text: "Dải động lệch mạnh về 0.\n\n", options: { color: COLOR.SLATE_DARK } },
    { text: "• log(STE) phi tuyến:\n", options: { bold: true, color: COLOR.ORANGE_DARK } },
    { text: "Kéo dãn phân bố im lặng.\n\n", options: { color: COLOR.SLATE_DARK } },
    { text: "• Tách rõ 2 đỉnh:\n", options: { bold: true, color: COLOR.GREEN_ACCENT } },
    { text: "Tạo thung lũng rõ ràng để đặt ngưỡng.", options: { color: COLOR.SLATE_DARK } }
  ], {
    x: 6.85,
    y: 1.7,
    w: 2.5,
    h: 3.1,
    fontSize: 18,
    fontFace: FONT_PRIMARY,
    margin: 0
  });

  slide.addNotes("So sánh giữa STE tuyến tính và log(STE): Thang đo log kéo dãn vùng năng lượng thấp của khoảng lặng, tạo thành 2 đỉnh phân bố tách biệt rõ rệt.");
}

// -------------------------------------------------------------
// SLIDE 5: TT1 - TÌM KIẾM NHỊ PHÂN
// -------------------------------------------------------------
{
  const slide = pres.addSlide();
  applySlideChrome(slide, 5);
  addSlideHeader(slide, "4. THUẬT TOÁN 1: TÌM KIẾM NHỊ PHÂN (TT1)", "Tối ưu hóa Sai số Biên thời gian bằng Phân đôi Không gian Ngưỡng");

  const imgPath = path.join(__dirname, "../assets/presentation/fig_tt1_binary_flow.png");
  if (fs.existsSync(imgPath)) {
    slide.addImage({
      path: imgPath,
      x: 0.5,
      y: 1.1,
      w: 5.6,
      h: 3.9
    });
  }

  slide.addShape(pres.ShapeType.roundRect, {
    x: 6.3,
    y: 1.1,
    w: 3.2,
    h: 3.9,
    rectRadius: 0.1,
    fill: { color: COLOR.BG_CARD },
    line: { color: COLOR.CYAN_ACCENT, width: 1.5 }
  });

  slide.addText("KẾT QUẢ HUẤN LUYỆN", {
    x: 6.5,
    y: 1.25,
    w: 2.8,
    h: 0.35,
    fontSize: 16,
    fontFace: FONT_PRIMARY,
    bold: true,
    color: COLOR.CYAN_DARK
  });

  slide.addText([
    { text: "• Khoảng tìm kiếm: ", options: { bold: true, color: COLOR.SLATE_DARK } },
    { text: "[0.0, 1.0]\n", options: { color: COLOR.SLATE_DARK } },
    { text: "• Số vòng lặp: ", options: { bold: true, color: COLOR.SLATE_DARK } },
    { text: "12 bước\n", options: { color: COLOR.SLATE_DARK } },
    { text: "• Độ mịn ngưỡng: ", options: { bold: true, color: COLOR.SLATE_DARK } },
    { text: "1/2^12 ≈ 0.00024\n", options: { color: COLOR.SLATE_DARK } },
    { text: "• Ngưỡng tối ưu: ", options: { bold: true, color: COLOR.ORANGE_DARK } },
    { text: "T = 0.000798\n", options: { bold: true, color: COLOR.ORANGE_DARK } },
    { text: "• Hàm mất mát: ", options: { bold: true, color: COLOR.GREEN_ACCENT } },
    { text: "Tổng sai số khung nhỏ nhất", options: { color: COLOR.SLATE_DARK } }
  ], {
    x: 6.5,
    y: 1.75,
    w: 2.8,
    h: 3.0,
    fontSize: 18,
    fontFace: FONT_PRIMARY,
    lineSpacing: 24,
    margin: 0
  });

  slide.addNotes("Thuật toán 1 tìm kiếm nhị phân chia đôi khoảng ngưỡng qua 12 vòng lặp trên tập huấn luyện, đạt ngưỡng tối ưu T = 0.000798 với tổng sai số thấp nhất.");
}

// -------------------------------------------------------------
// SLIDE 6: TT2 - PHÂN TÍCH HISTOGRAM LOG(STE)
// -------------------------------------------------------------
{
  const slide = pres.addSlide();
  applySlideChrome(slide, 6);
  addSlideHeader(slide, "5. THUẬT TOÁN 2: PHÂN TÍCH HISTOGRAM (TT2)", "Xác định Đáy Thung lũng giữa 2 Đỉnh Cực đại Năng lượng Phi tuyến");

  const imgPath = path.join(__dirname, "../assets/presentation/fig_tt2_histogram_flow.png");
  if (fs.existsSync(imgPath)) {
    slide.addImage({
      path: imgPath,
      x: 0.5,
      y: 1.1,
      w: 5.6,
      h: 3.9
    });
  }

  slide.addShape(pres.ShapeType.roundRect, {
    x: 6.3,
    y: 1.1,
    w: 3.2,
    h: 3.9,
    rectRadius: 0.1,
    fill: { color: COLOR.BG_CARD },
    line: { color: COLOR.ORANGE_ACCENT, width: 1.5 }
  });

  slide.addText("KẾT QUẢ HUẤN LUYỆN", {
    x: 6.5,
    y: 1.25,
    w: 2.8,
    h: 0.35,
    fontSize: 16,
    fontFace: FONT_PRIMARY,
    bold: true,
    color: COLOR.ORANGE_DARK
  });

  slide.addText([
    { text: "• Không gian: ", options: { bold: true, color: COLOR.SLATE_DARK } },
    { text: "log(STE)\n", options: { color: COLOR.SLATE_DARK } },
    { text: "• Số bins: ", options: { bold: true, color: COLOR.SLATE_DARK } },
    { text: "Histogram đa mức\n", options: { color: COLOR.SLATE_DARK } },
    { text: "• Trọng số lệch: ", options: { bold: true, color: COLOR.SLATE_DARK } },
    { text: "W = 2.0 (nghiêng về silence)\n", options: { color: COLOR.SLATE_DARK } },
    { text: "• Ngưỡng tối ưu: ", options: { bold: true, color: COLOR.ORANGE_DARK } },
    { text: "T = -2.4375\n", options: { bold: true, color: COLOR.ORANGE_DARK } },
    { text: "• Kháng nhiễu: ", options: { bold: true, color: COLOR.GREEN_ACCENT } },
    { text: "Tối ưu nhất cho môi trường Phone", options: { color: COLOR.SLATE_DARK } }
  ], {
    x: 6.5,
    y: 1.75,
    w: 2.8,
    h: 3.0,
    fontSize: 18,
    fontFace: FONT_PRIMARY,
    lineSpacing: 24,
    margin: 0
  });

  slide.addNotes("Thuật toán 2 lập biểu đồ Histogram trên log(STE), phát hiện 2 cực đại và xác định đáy thung lũng với trọng số W = 2.0, mang lại ngưỡng T = -2.4375.");
}

// -------------------------------------------------------------
// SLIDE 7: TT3 - PHÂN PHỐI CHUẨN GAUSSIAN BAYES
// -------------------------------------------------------------
{
  const slide = pres.addSlide();
  applySlideChrome(slide, 7);
  addSlideHeader(slide, "6. THUẬT TOÁN 3: PHÂN PHỐI GAUSS BAYES (TT3)", "Phân loại Thống kê Mô hình hóa Hàm Mật độ Xác suất (PDF)");

  const imgPath = path.join(__dirname, "../assets/presentation/fig_tt3_gaussian_flow.png");
  if (fs.existsSync(imgPath)) {
    slide.addImage({
      path: imgPath,
      x: 0.5,
      y: 1.1,
      w: 5.6,
      h: 3.9
    });
  }

  slide.addShape(pres.ShapeType.roundRect, {
    x: 6.3,
    y: 1.1,
    w: 3.2,
    h: 3.9,
    rectRadius: 0.1,
    fill: { color: COLOR.BG_CARD },
    line: { color: COLOR.GREEN_ACCENT, width: 1.5 }
  });

  slide.addText("KẾT QUẢ HUẤN LUYỆN", {
    x: 6.5,
    y: 1.25,
    w: 2.8,
    h: 0.35,
    fontSize: 16,
    fontFace: FONT_PRIMARY,
    bold: true,
    color: COLOR.GREEN_ACCENT
  });

  slide.addText([
    { text: "• Silence: ", options: { bold: true, color: COLOR.SLATE_DARK } },
    { text: "mu=0.00025, sigma=0.00063\n", options: { color: COLOR.SLATE_DARK } },
    { text: "• Speech: ", options: { bold: true, color: COLOR.SLATE_DARK } },
    { text: "mu=0.20247, sigma=0.23569\n", options: { color: COLOR.SLATE_DARK } },
    { text: "• Chuẩn Bayes: ", options: { bold: true, color: COLOR.CYAN_DARK } },
    { text: "Điểm giao xác suất 2 lớp\n", options: { color: COLOR.SLATE_DARK } },
    { text: "• Ngưỡng tối ưu: ", options: { bold: true, color: COLOR.ORANGE_DARK } },
    { text: "T = 0.000792\n", options: { bold: true, color: COLOR.ORANGE_DARK } },
    { text: "• Tương đồng TT1: ", options: { bold: true, color: COLOR.GREEN_ACCENT } },
    { text: "Hội tụ về cùng mức năng lượng", options: { color: COLOR.SLATE_DARK } }
  ], {
    x: 6.5,
    y: 1.75,
    w: 2.8,
    h: 3.0,
    fontSize: 18,
    fontFace: FONT_PRIMARY,
    lineSpacing: 24,
    margin: 0
  });

  slide.addNotes("Thuật toán 3 mô hình hóa xác suất bằng phân phối chuẩn cho cả hai trạng thái. Giao điểm của hai đường phân phối xác suất mang lại ngưỡng Bayes T = 0.000792.");
}

// -------------------------------------------------------------
// SLIDE 8: TỔNG HỢP NGƯỠNG TOÀN CỤC HUẤN LUYỆN
// -------------------------------------------------------------
{
  const slide = pres.addSlide();
  applySlideChrome(slide, 8);
  addSlideHeader(slide, "7. TỔNG HỢP NGƯỠNG TRÊN TẬP HUẤN LUYỆN", "So sánh Cơ chế Hội tụ và Ngưỡng Toàn cục của 03 Thuật toán");

  const imgPath = path.join(__dirname, "../assets/presentation/fig_training_summary.png");
  if (fs.existsSync(imgPath)) {
    slide.addImage({
      path: imgPath,
      x: 0.5,
      y: 1.1,
      w: 9.0,
      h: 4.0
    });
  }

  slide.addNotes("Tổng hợp trên tập huấn luyện: Cả 3 phương pháp đều hội tụ nhanh chóng. TT1 và TT3 cho ngưỡng tuyến tính gần như trùng khớp, trong khi TT2 đạt MAE huấn luyện thấp nhất.");
}

// -------------------------------------------------------------
// SLIDE 9: KẾT QUẢ TT1 TRÊN 4 FILE TEST
// -------------------------------------------------------------
{
  const slide = pres.addSlide();
  applySlideChrome(slide, 9);
  addSlideHeader(slide, "8. KẾT QUẢ THỰC NGHIỆM TT1: BINARY SEARCH", "Đánh giá trên 04 File Kiểm thử — Ngưỡng Toàn cục T = 0.000798");

  const imgPath = path.join(__dirname, "../assets/presentation/fig_test_binary_4files.png");
  if (fs.existsSync(imgPath)) {
    slide.addImage({
      path: imgPath,
      x: 0.5,
      y: 1.1,
      w: 9.0,
      h: 4.0
    });
  }

  slide.addNotes("Kết quả kiểm thử TT1: Biên thuật toán màu xanh bám sát biên chuẩn màu đỏ. F0 xuất hiện chuẩn xác bên trong vùng tiếng nói. Studio F2 đạt MAE xuất sắc 2.49 ms.");
}

// -------------------------------------------------------------
// SLIDE 10: KẾT QUẢ TT2 TRÊN 4 FILE TEST
// -------------------------------------------------------------
{
  const slide = pres.addSlide();
  applySlideChrome(slide, 10);
  addSlideHeader(slide, "9. KẾT QUẢ THỰC NGHIỆM TT2: HISTOGRAM LOG(STE)", "Đánh giá trên 04 File Kiểm thử — Ngưỡng Toàn cục T = -2.4375 (W=2.0)");

  const imgPath = path.join(__dirname, "../assets/presentation/fig_test_histogram_4files.png");
  if (fs.existsSync(imgPath)) {
    slide.addImage({
      path: imgPath,
      x: 0.5,
      y: 1.1,
      w: 9.0,
      h: 4.0
    });
  }

  slide.addNotes("Kết quả kiểm thử TT2: Biểu diễn log(STE) giúp giữ vững ranh giới âm thanh trong môi trường phone_F2, giảm sai số từ 62.5 ms xuống còn 45.0 ms.");
}

// -------------------------------------------------------------
// SLIDE 11: KẾT QUẢ TT3 TRÊN 4 FILE TEST
// -------------------------------------------------------------
{
  const slide = pres.addSlide();
  applySlideChrome(slide, 11);
  addSlideHeader(slide, "10. KẾT QUẢ THỰC NGHIỆM TT3: GAUSSIAN BAYES", "Đánh giá trên 04 File Kiểm thử — Ngưỡng Toàn cục T = 0.000792");

  const imgPath = path.join(__dirname, "../assets/presentation/fig_test_gaussian_4files.png");
  if (fs.existsSync(imgPath)) {
    slide.addImage({
      path: imgPath,
      x: 0.5,
      y: 1.1,
      w: 9.0,
      h: 4.0
    });
  }

  slide.addNotes("Kết quả kiểm thử TT3: Tương đương TT1 do ngưỡng Bayes hội tụ tại 0.000792. Phân đoạn rất hoàn hảo ở môi trường Studio.");
}

// -------------------------------------------------------------
// SLIDE 12: ĐÁNH GIÁ MÔI TRƯỜNG STUDIO
// -------------------------------------------------------------
{
  const slide = pres.addSlide();
  applySlideChrome(slide, 12);
  addSlideHeader(slide, "11. ĐÁNH GIÁ MÔI TRƯỜNG PHÒNG THU (STUDIO)", "Tín hiệu Tinh sạch High SNR (37.7 - 49.3 dB) — Độ chính xác Tuyệt đối");

  const imgPath = path.join(__dirname, "../assets/presentation/fig_studio_deepdive.png");
  if (fs.existsSync(imgPath)) {
    slide.addImage({
      path: imgPath,
      x: 0.5,
      y: 1.1,
      w: 6.2,
      h: 3.9
    });
  }

  slide.addShape(pres.ShapeType.roundRect, {
    x: 6.9,
    y: 1.1,
    w: 2.6,
    h: 3.9,
    rectRadius: 0.1,
    fill: { color: COLOR.BG_CARD },
    line: { color: COLOR.CYAN_ACCENT, width: 1.5 }
  });

  slide.addText("ĐẶC TÍNH STUDIO", {
    x: 7.05,
    y: 1.25,
    w: 2.3,
    h: 0.35,
    fontSize: 15,
    fontFace: FONT_PRIMARY,
    bold: true,
    color: COLOR.CYAN_DARK
  });

  slide.addText([
    { text: "• SNR cực cao:\n", options: { bold: true, color: COLOR.CYAN_DARK } },
    { text: "Studio F2: 49.3 dB\nStudio M2: 37.7 dB\n\n", options: { color: COLOR.SLATE_DARK } },
    { text: "• Sai số cực thấp:\n", options: { bold: true, color: COLOR.GREEN_ACCENT } },
    { text: "MAE chỉ từ 2.49 đến 12.49 ms\n\n", options: { bold: true, color: COLOR.GREEN_ACCENT } },
    { text: "• Kết luận:\n", options: { bold: true, color: COLOR.SLATE_DARK } },
    { text: "Cả 3 thuật toán đều phân đoạn hoàn hảo.", options: { color: COLOR.SLATE_MUTED } }
  ], {
    x: 7.05,
    y: 1.7,
    w: 2.3,
    h: 3.1,
    fontSize: 18,
    fontFace: FONT_PRIMARY,
    margin: 0
  });

  slide.addNotes("Môi trường phòng thu có tỉ số SNR rất cao, ranh giới năng lượng dốc đứng giúp cả 3 thuật toán đạt độ chính xác gần như tuyệt đối với MAE chỉ vài mili giây.");
}

// -------------------------------------------------------------
// SLIDE 13: ĐÁNH GIÁ MÔI TRƯỜNG PHONE
// -------------------------------------------------------------
{
  const slide = pres.addSlide();
  applySlideChrome(slide, 13);
  addSlideHeader(slide, "12. ĐÁNH GIÁ MÔI TRƯỜNG ĐIỆN THOẠI (PHONE)", "Tín hiệu Nhiễu nền Low SNR (24.8 - 27.0 dB) — Ưu thế Kháng nhiễu");

  const imgPath = path.join(__dirname, "../assets/presentation/fig_phone_deepdive.png");
  if (fs.existsSync(imgPath)) {
    slide.addImage({
      path: imgPath,
      x: 0.5,
      y: 1.1,
      w: 6.2,
      h: 3.9
    });
  }

  slide.addShape(pres.ShapeType.roundRect, {
    x: 6.9,
    y: 1.1,
    w: 2.6,
    h: 3.9,
    rectRadius: 0.1,
    fill: { color: COLOR.BG_CARD },
    line: { color: COLOR.ORANGE_ACCENT, width: 1.5 }
  });

  slide.addText("TÁC ĐỘNG CỦA NHIỄU", {
    x: 7.05,
    y: 1.25,
    w: 2.3,
    h: 0.35,
    fontSize: 15,
    fontFace: FONT_PRIMARY,
    bold: true,
    color: COLOR.ORANGE_DARK
  });

  slide.addText([
    { text: "• SNR thấp:\n", options: { bold: true, color: COLOR.ORANGE_DARK } },
    { text: "Phone M2: 27.0 dB\nPhone F2: 24.8 dB\n\n", options: { color: COLOR.SLATE_DARK } },
    { text: "• TT2 vượt trội:\n", options: { bold: true, color: COLOR.GREEN_ACCENT } },
    { text: "MAE chỉ 27.5 ms (so với 35.0 ms của TT1/TT3)\n\n", options: { bold: true, color: COLOR.GREEN_ACCENT } },
    { text: "• Lý do:\n", options: { bold: true, color: COLOR.SLATE_DARK } },
    { text: "Không gian log nén nhiễu nền hiệu quả.", options: { color: COLOR.SLATE_MUTED } }
  ], {
    x: 7.05,
    y: 1.7,
    w: 2.3,
    h: 3.1,
    fontSize: 18,
    fontFace: FONT_PRIMARY,
    margin: 0
  });

  slide.addNotes("Môi trường điện thoại có mức nhiễu nền đáng kể. Thuật toán 2 Histogram trên log(STE) thể hiện tính vượt trội rõ rệt khi giảm đáng kể sai số phân đoạn.");
}

// -------------------------------------------------------------
// SLIDE 14: SO SÁNH ĐỊNH LƯỢNG TOÀN DIỆN & BIỂU ĐỒ SNR
// -------------------------------------------------------------
{
  const slide = pres.addSlide();
  applySlideChrome(slide, 14);
  addSlideHeader(slide, "13. TỔNG HỢP ĐỊNH LƯỢNG & TÁC ĐỘNG CỦA SNR", "Đối chiếu Sai số MAE/RMSE giữa 03 Thuật toán trên Toàn bộ Tập Kiểm thử");

  const imgPath = path.join(__dirname, "../assets/presentation/fig_snr_comparison.png");
  if (fs.existsSync(imgPath)) {
    slide.addImage({
      path: imgPath,
      x: 0.5,
      y: 1.1,
      w: 5.6,
      h: 3.9
    });
  }

  // Right card: Bảng số liệu cô đọng
  slide.addShape(pres.ShapeType.roundRect, {
    x: 6.3,
    y: 1.1,
    w: 3.2,
    h: 3.9,
    rectRadius: 0.1,
    fill: { color: COLOR.BG_CARD },
    line: { color: COLOR.BORDER_CARD, width: 1.0 }
  });

  slide.addText("BẢNG SAI SỐ TRUNG BÌNH", {
    x: 6.45,
    y: 1.25,
    w: 2.9,
    h: 0.35,
    fontSize: 15,
    fontFace: FONT_PRIMARY,
    bold: true,
    color: COLOR.ORANGE_ACCENT
  });

  slide.addText([
    { text: "• Môi trường Studio:\n", options: { bold: true, color: COLOR.CYAN_DARK } },
    { text: "TT1: 7.49 ms | TT2: 8.75 ms\n\n", options: { color: COLOR.SLATE_DARK } },
    { text: "• Môi trường Phone:\n", options: { bold: true, color: COLOR.ORANGE_DARK } },
    { text: "TT1: 35.0 ms | TT2: 27.5 ms\n\n", options: { color: COLOR.SLATE_DARK } },
    { text: "• Toàn bộ 04 file:\n", options: { bold: true, color: COLOR.GREEN_ACCENT } },
    { text: "TT1: 21.25 ms\nTT2: 18.12 ms (Tốt nhất)\nTT3: 21.25 ms", options: { bold: true, color: COLOR.GREEN_ACCENT } }
  ], {
    x: 6.45,
    y: 1.7,
    w: 2.9,
    h: 3.1,
    fontSize: 18,
    fontFace: FONT_PRIMARY,
    margin: 0
  });

  slide.addNotes("Nhìn vào biểu đồ so sánh: Ở phòng thu, cả 3 thuật toán đều đạt MAE 7-8 ms. Nhưng ở môi trường điện thoại có nhiễu, Histogram log(STE) vượt trội với MAE chỉ 27.5 ms so với 35 ms.");
}

// -------------------------------------------------------------
// SLIDE 15: KẾT LUẬN & HƯỚNG MỞ RỘNG NGƯỠNG KÉP ZCR
// -------------------------------------------------------------
{
  const slide = pres.addSlide();
  applySlideChrome(slide, 15);
  addSlideHeader(slide, "14. KẾT LUẬN & HƯỚNG MỞ RỘNG NGƯỠNG KÉP", "Giải pháp Khắc phục Âm Vô thanh bằng Zero Crossing Rate (ZCR)");

  const imgPath = path.join(__dirname, "../assets/presentation/fig_zcr_concept.png");
  if (fs.existsSync(imgPath)) {
    slide.addImage({
      path: imgPath,
      x: 0.5,
      y: 1.1,
      w: 9.0,
      h: 4.0
    });
  }

  slide.addNotes("Kết luận: Histogram trên log(STE) là giải pháp tối ưu nhất cho bài toán ngưỡng đơn. Nguyên nhân sai số chủ yếu rơi vào âm vô thanh mang năng lượng thấp. Hướng phát triển tiếp theo là kết hợp ngưỡng kép STE và ZCR.");
}

// -------------------------------------------------------------
// XUẤT FILE PRESENTATION
// -------------------------------------------------------------
const outputFilePath = path.join(__dirname, "../presentation_speech_silence.pptx");
pres.writeFile({ fileName: outputFilePath })
  .then(() => {
    console.log(`=== ĐÃ XUẤT THÀNH CÔNG BỘ SLIDE 15 TRANG: ${outputFilePath} ===`);
  })
  .catch(err => {
    console.error("Lỗi khi ghi file PPTX:", err);
  });
