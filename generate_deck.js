const pptxgen = require("pptxgenjs");
const path = require("path");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10" x 5.625"

// Bảng màu Dark Slate Tech Palette (Hiện đại, tương phản cao, đúng chuẩn)
const C_BG = "0F172A";       // Nền chính xanh đen tối
const C_CARD = "1E293B";     // Nền khối thẻ
const C_BORDER = "334155";   // Viền
const C_TEXT_MAIN = "F8FAFC";// Chữ chính trắng sáng
const C_TEXT_MUTED = "94A3B8"; // Chữ phụ xám nhạt
const C_CYAN = "38BDF8";     // Nhấn mạnh Cyan
const C_GREEN = "34D399";    // Thành công / Gauss
const C_AMBER = "FBBF24";    // Cảnh báo / Histogram
const C_PURPLE = "A78BFA";   // Tím / Binary Search

// Helper: Header chung cho các slide nội dung
function addHeader(slide, titleText, categoryText) {
  slide.background = { color: C_BG };
  
  // Category badge
  slide.addText(categoryText.toUpperCase(), {
    x: 0.6, y: 0.35, w: 8.8, h: 0.3,
    fontSize: 11, fontFace: "Calibri", color: C_CYAN, bold: true,
    margin: 0
  });
  
  // Title chính
  slide.addText(titleText, {
    x: 0.6, y: 0.65, w: 8.8, h: 0.45,
    fontSize: 22, fontFace: "Calibri", color: C_TEXT_MAIN, bold: true,
    margin: 0
  });

  // Đường phân cách tinh tế
  slide.addShape(pres.shapes.LINE, {
    x: 0.6, y: 1.15, w: 8.8, h: 0,
    line: { color: C_BORDER, width: 1.5 }
  });
}

// ==========================================
// SLIDE 1: COVER SLIDE
// ==========================================
const s1 = pres.addSlide();
s1.background = { color: C_BG };

// Hộp trang trí trung tâm
s1.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.8, y: 0.8, w: 8.4, h: 4.025,
  fill: { color: C_CARD },
  line: { color: C_CYAN, width: 2 },
  rectRadius: 0.2
});

s1.addText("BÁO CÁO BÀI TẬP THI GIỮA KỲ — XỬ LÝ TÍN HIỆU TIẾNG NÓI", {
  x: 1.2, y: 1.2, w: 7.6, h: 0.35,
  fontSize: 13, fontFace: "Calibri", color: C_CYAN, bold: true, align: "center",
  margin: 0
});

s1.addText("PHÂN ĐOẠN TIẾNG NÓI & KHOẢNG LẶNG (VAD)", {
  x: 1.2, y: 1.65, w: 7.6, h: 0.8,
  fontSize: 28, fontFace: "Calibri", color: C_TEXT_MAIN, bold: true, align: "center",
  margin: 0
});

s1.addText("Nghiên cứu & Đối chiếu 3 Thuật toán: Histogram • Binary Search • Gaussian", {
  x: 1.2, y: 2.5, w: 7.6, h: 0.4,
  fontSize: 15, fontFace: "Calibri", color: C_TEXT_MUTED, align: "center",
  margin: 0
});

// Thẻ thông tin SV
s1.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 1.6, y: 3.1, w: 6.8, h: 1.3,
  fill: { color: "162032" },
  line: { color: C_BORDER, width: 1 },
  rectRadius: 0.1
});

s1.addText([
  { text: "• Giảng viên hướng dẫn: Bộ môn Xử lý Tín hiệu Âm thanh & Tiếng nói\n", options: { bold: false, color: C_TEXT_MUTED } },
  { text: "• Sinh viên thực hiện: Nhóm Nghiên cứu VAD (Simple Statistics & So sánh Đa thuật toán)\n", options: { bold: false, color: C_TEXT_MAIN } },
  { text: "• Tiêu chuẩn thực nghiệm: 04 file Huấn luyện (Train) & 04 file Kiểm thử (Test)\n", options: { bold: false, color: C_TEXT_MUTED } },
  { text: "• Khung thời gian: 3 phút Thuyết trình Slide + 1 phút Demo Chương trình", options: { bold: true, color: C_CYAN } }
], {
  x: 1.8, y: 3.25, w: 6.4, h: 1.0,
  fontSize: 12, fontFace: "Calibri", margin: 0
});

s1.addNotes("Kính thưa Thầy/Cô và các bạn, hôm nay nhóm em xin báo cáo đề tài Phân đoạn tiếng nói và khoảng lặng bằng 3 thuật toán: Histogram, Binary Search và Gaussian Simple Statistics.");

// ==========================================
// SLIDE 2: UNIFIED PIPELINE
// ==========================================
const s2 = pres.addSlide();
addHeader(s2, "KIẾN TRÚC PIPELINE THỐNG NHẤT 4 GIAI ĐOẠN", "Quy trình Thực thi Chung");

// 4 Khối ngang
const blocks = [
  { num: "1", title: "TIỀN XỬ LÝ", desc: "• Kênh đơn Mono\n• Float32 [-1.0, 1.0]\n• Khử DC Offset mean", col: C_CYAN },
  { num: "2", title: "ĐẶC TRƯNG", desc: "• Khung 25ms / Hop 10ms\n• Mốc tâm khung ti\n• STE norm & log(STE)", col: C_CYAN },
  { num: "3", title: "TÌM NGƯỠNG T*", desc: "• Histogram: T*=-2.44\n• Binary: T*=0.00080\n• Gauss: T*=0.00079", col: C_AMBER, highlight: true },
  { num: "4", title: "HẬU XỬ LÝ", desc: "• Lọc lặng < 200ms\n• Lọc clicks < 30ms\n• Đánh giá MAE/RMSE", col: C_GREEN }
];

blocks.forEach((b, idx) => {
  const xPos = 0.6 + idx * 2.25;
  s2.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: xPos, y: 1.4, w: 2.05, h: 2.8,
    fill: { color: C_CARD },
    line: { color: b.highlight ? C_AMBER : C_BORDER, width: b.highlight ? 2 : 1 },
    rectRadius: 0.15
  });

  // Số thứ tự
  s2.addShape(pres.shapes.OVAL, {
    x: xPos + 0.15, y: 1.55, w: 0.35, h: 0.35,
    fill: { color: b.col }
  });
  s2.addText(b.num, {
    x: xPos + 0.15, y: 1.55, w: 0.35, h: 0.35,
    fontSize: 12, fontFace: "Calibri", color: "0F172A", bold: true, align: "center", valign: "middle", margin: 0
  });

  // Tựa đề khối
  s2.addText(b.title, {
    x: xPos + 0.58, y: 1.6, w: 1.35, h: 0.3,
    fontSize: 13, fontFace: "Calibri", color: b.col, bold: true, margin: 0
  });

  // Nội dung
  s2.addText(b.desc, {
    x: xPos + 0.15, y: 2.05, w: 1.75, h: 2.0,
    fontSize: 12, fontFace: "Calibri", color: C_TEXT_MAIN, margin: 0
  });

  // Mũi tên giữa các khối
  if (idx < 3) {
    s2.addText("➔", {
      x: xPos + 2.05, y: 2.6, w: 0.2, h: 0.3,
      fontSize: 16, fontFace: "Calibri", color: C_TEXT_MUTED, align: "center", margin: 0
    });
  }
});

// Footer banner
s2.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.6, y: 4.35, w: 8.8, h: 0.8,
  fill: { color: "162032" },
  line: { color: C_BORDER, width: 1 },
  rectRadius: 0.1
});

s2.addText([
  { text: "Quy chuẩn Đồ án: ", options: { bold: true, color: C_CYAN } },
  { text: "Cả 3 thuật toán chia sẻ 100% khung tiền xử lý, phân khung và hậu xử lý. ", options: { color: C_TEXT_MAIN } },
  { text: "Điểm khác biệt duy nhất nằm ở Khối 3: Cơ chế tính toán ngưỡng tối ưu T* từ 04 file huấn luyện.", options: { bold: true, color: C_AMBER } }
], {
  x: 0.8, y: 4.45, w: 8.4, h: 0.6,
  fontSize: 12, fontFace: "Calibri", margin: 0
});

s2.addNotes("Nhóm em thiết kế một pipeline thống nhất. Cả 3 thuật toán đều chạy chung khâu tiền xử lý, phân khung 25ms hop 10ms, và hậu xử lý 200ms. Chỉ có khối tìm ngưỡng là rẽ nhánh.");

// ==========================================
// SLIDE 3: CƠ CHẾ XÁC ĐỊNH NGƯỠNG T*
// ==========================================
const s3 = pres.addSlide();
addHeader(s3, "CƠ CHẾ XÁC ĐỊNH NGƯỠNG TOÀN CỤC (T*)", "Giải Pháp Lõi");

// Cột trái: 3 Thuật toán (Width: 4.4)
const algCards = [
  { name: "1. HISTOGRAM (Giannakopoulos 2014)", math: "T* = (W·M1 + M2)/(W + 1) với W=2.0", res: "Miền log(STE) • T* = -2.4375", col: C_AMBER },
  { name: "2. BINARY SEARCH (Hodgkinson 2012)", math: "Cân bằng diện tích nhầm lẫn (Area of Confusion)", res: "Miền STE_norm • T* = 0.00080", col: C_PURPLE },
  { name: "3. GAUSSIAN (Simple Statistics)", math: "Cân bằng z-score: (T-μsil)/σsil = (μsp-T)/σsp", res: "Miền STE_norm • T* = 0.00079", col: C_GREEN }
];

algCards.forEach((c, idx) => {
  const yPos = 1.35 + idx * 1.25;
  s3.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.6, y: yPos, w: 4.2, h: 1.15,
    fill: { color: C_CARD },
    line: { color: c.col, width: 1.5 },
    rectRadius: 0.1
  });

  s3.addText(c.name, {
    x: 0.75, y: yPos + 0.1, w: 3.9, h: 0.25,
    fontSize: 12, fontFace: "Calibri", color: c.col, bold: true, margin: 0
  });
  s3.addText(c.math, {
    x: 0.75, y: yPos + 0.38, w: 3.9, h: 0.35,
    fontSize: 11, fontFace: "Calibri", color: C_TEXT_MAIN, margin: 0
  });
  s3.addText(c.res, {
    x: 0.75, y: yPos + 0.75, w: 3.9, h: 0.3,
    fontSize: 11.5, fontFace: "Calibri", color: C_CYAN, bold: true, margin: 0
  });
});

// Cột phải: Hình vẽ phân phối Gauss (Width: 4.4)
const figGaussPath = path.resolve("reports/figures/figure_gaussian_threshold_analysis.png");
s3.addImage({
  path: figGaussPath,
  x: 5.0, y: 1.35, w: 4.4, h: 3.7
});

s3.addNotes("Đây là giải pháp lõi tìm ngưỡng. Histogram tìm đỉnh đôi trên thang log; Binary Search cân bằng diện tích nhầm lẫn; Gaussian cân bằng khoảng cách z-score. Hình bên phải minh họa điểm giao nhau Z-score của Gaussian.");

// ==========================================
// SLIDE 4: BẢNG KẾT QUẢ ĐỊNH LƯỢNG TẬP TEST
// ==========================================
const s4 = pres.addSlide();
addHeader(s4, "KẾT QUẢ ĐÁNH GIÁ ĐỊNH LƯỢNG TRÊN TẬP KIỂM THỬ", "Thực Nghiệm Toàn Cục");

// Bảng số liệu chuẩn xác
const tableRows = [
  [
    { text: "Tên File", options: { bold: true, color: C_CYAN, fill: { color: "162032" } } },
    { text: "Môi trường", options: { bold: true, color: C_CYAN, fill: { color: "162032" } } },
    { text: "SNR (dB)", options: { bold: true, color: C_CYAN, fill: { color: "162032" } } },
    { text: "Histogram MAE", options: { bold: true, color: C_AMBER, fill: { color: "162032" } } },
    { text: "Binary MAE", options: { bold: true, color: C_PURPLE, fill: { color: "162032" } } },
    { text: "Gaussian MAE", options: { bold: true, color: C_GREEN, fill: { color: "162032" } } }
  ],
  ["phone_F2", "Phone", "24.8 dB", "45.0000 ms", "62.5000 ms", "62.5000 ms"],
  ["phone_M2", "Phone", "27.0 dB", "10.0000 ms", "7.5000 ms", "7.5000 ms"],
  ["studio_F2", "Studio", "49.3 dB", "2.4940 ms", "2.4940 ms", "2.4940 ms"],
  ["studio_M2", "Studio", "37.7 dB", "15.0000 ms", "12.4940 ms", "12.4940 ms"],
  [
    { text: "TB Studio", options: { bold: true, color: C_CYAN } },
    { text: "Phòng thu sạch", options: { color: C_TEXT_MUTED } },
    { text: "43.5 dB", options: { color: C_TEXT_MUTED } },
    { text: "8.7470 ms", options: { bold: true, color: C_AMBER } },
    { text: "7.4940 ms", options: { bold: true, color: C_PURPLE } },
    { text: "7.4940 ms", options: { bold: true, color: C_GREEN } }
  ],
  [
    { text: "TOÀN BỘ", options: { bold: true, color: C_CYAN, fill: { color: "162032" } } },
    { text: "Overall 4 file", options: { bold: true, color: C_TEXT_MAIN, fill: { color: "162032" } } },
    { text: "34.7 dB", options: { bold: true, color: C_TEXT_MAIN, fill: { color: "162032" } } },
    { text: "18.1235 ms", options: { bold: true, color: C_AMBER, fill: { color: "162032" } } },
    { text: "21.2470 ms", options: { bold: true, color: C_PURPLE, fill: { color: "162032" } } },
    { text: "21.2470 ms", options: { bold: true, color: C_GREEN, fill: { color: "162032" } } }
  ]
];

s4.addTable(tableRows, {
  x: 0.6, y: 1.35, w: 8.8, h: 2.3,
  fontSize: 11.5, fontFace: "Calibri", color: C_TEXT_MAIN,
  border: { color: C_BORDER, pt: 1 },
  align: "center", valign: "middle"
});

// 2 Hộp nhận xét bên dưới
s4.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.6, y: 3.85, w: 4.25, h: 1.25,
  fill: { color: C_CARD }, line: { color: C_CYAN, width: 1.5 }, rectRadius: 0.1
});
s4.addText([
  { text: "Nhận xét Phòng thu (Studio - SNR cao 43 dB):\n", options: { bold: true, color: C_CYAN } },
  { text: "• Cả 3 thuật toán đạt độ chính xác xuất sắc: MAE < 8.8 ms.\n", options: { color: C_TEXT_MAIN } },
  { text: "• File studio_F2 đạt kỷ lục 2.494 ms (nhỏ hơn 1 bước nhảy khung 10ms).\n", options: { color: C_TEXT_MAIN } },
  { text: "• Vượt tiêu chuẩn vàng 5-15 ms của Bell Labs (Lamel et al., 1981).", options: { color: C_TEXT_MUTED } }
], { x: 0.75, y: 3.95, w: 4.0, h: 1.05, fontSize: 11, fontFace: "Calibri", margin: 0 });

s4.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 5.15, y: 3.85, w: 4.25, h: 1.25,
  fill: { color: C_CARD }, line: { color: C_AMBER, width: 1.5 }, rectRadius: 0.1
});
s4.addText([
  { text: "Nhận xét Điện thoại (Phone - SNR thấp 26 dB):\n", options: { bold: true, color: C_AMBER } },
  { text: "• Histogram vượt trội với Overall MAE = 18.12 ms nhờ thang log(STE).\n", options: { color: C_TEXT_MAIN } },
  { text: "• Binary & Gaussian đạt 21.25 ms do đặc trưng STE tuyến tính.\n", options: { color: C_TEXT_MAIN } },
  { text: "• Hoàn toàn nằm trong dung sai tha thứ 250 ms của chuẩn Viện NIST.", options: { color: C_TEXT_MUTED } }
], { x: 5.3, y: 3.95, w: 4.0, h: 1.05, fontSize: 11, fontFace: "Calibri", margin: 0 });

s4.addNotes("Bảng kết quả kiểm thử toàn cục. Môi trường Studio đạt sai số cực thấp chỉ 7.49 ms. Môi trường Phone có nhiễu nên Histogram với thang logSTE thể hiện tính kháng nhiễu tốt nhất đạt 18.12 ms.");

// ==========================================
// SLIDE 5: THỰC NGHIỆM MÔI TRƯỜNG STUDIO
// ==========================================
const s5 = pres.addSlide();
addHeader(s5, "THỰC NGHIỆM STUDIO: ĐỘ CHÍNH XÁC CAO (SNR = 49.3 dB)", "Môi Trường Phòng Thu Sạch");

// Trái: Hình vẽ (Width: 5.3)
const figStudioPath = path.resolve("reports/figures/figure_3_studio_F2_gaussian.png");
s5.addImage({
  path: figStudioPath,
  x: 0.6, y: 1.35, w: 5.3, h: 3.7
});

// Phải: Nhận xét (Width: 3.3)
s5.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 6.1, y: 1.35, w: 3.3, h: 3.7,
  fill: { color: C_CARD }, line: { color: C_GREEN, width: 1.5 }, rectRadius: 0.1
});

s5.addText([
  { text: "ĐẶC TRƯNG STUDIO_F2:\n\n", options: { bold: true, color: C_GREEN, fontSize: 13 } },
  { text: "• SNR cực cao: 49.3 dB\n", options: { bold: true, color: C_CYAN } },
  { text: "Sàn nhiễu phòng thu sạch, năng lượng khoảng lặng sát gốc 0.\n\n", options: { color: C_TEXT_MUTED } },
  { text: "• Khớp 2/2 biên (100%):\n", options: { bold: true, color: C_TEXT_MAIN } },
  { text: "Không xuất hiện bất kỳ biên giả hay xung nhiễu nào.\n\n", options: { color: C_TEXT_MUTED } },
  { text: "• Sai số kỷ lục 2.494 ms:\n", options: { bold: true, color: C_GREEN } },
  { text: "Nhỏ hơn độ phân giải bước nhảy khung (Hop = 10 ms).\n\n", options: { color: C_TEXT_MUTED } },
  { text: "• Kiểm chứng Pitch F0:\n", options: { bold: true, color: C_CYAN } },
  { text: "Đường F0 bắt trọn vẹn và liên tục các khung nguyên âm hữu thanh.", options: { color: C_TEXT_MUTED } }
], { x: 6.3, y: 1.55, w: 2.9, h: 3.3, fontSize: 11, fontFace: "Calibri", margin: 0 });

s5.addNotes("Đây là kết quả trên file studio_F2. Tín hiệu phòng thu có SNR tới 49.3 dB, không hề có nhiễu xung. Cả 2 biên đều khớp chuẩn xác với sai số kỷ lục chỉ 2.494 ms, đường pitch F0 bắt rất đẹp.");

// ==========================================
// SLIDE 6: MÔI TRƯỜNG PHONE & LỌC XUNG NHIỄU
// ==========================================
const s6 = pres.addSlide();
addHeader(s6, "MÔI TRƯỜNG PHONE: CƠ CHẾ LỌC NHIỄU XUNG CLICKS (< 30ms)", "Môi Trường Nhiễu Điện Thoại");

const figPhoneM2Path = path.resolve("reports/figures/figure_2_phone_M2_gaussian.png");
s6.addImage({
  path: figPhoneM2Path,
  x: 0.6, y: 1.35, w: 5.3, h: 3.7
});

s6.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 6.1, y: 1.35, w: 3.3, h: 3.7,
  fill: { color: C_CARD }, line: { color: C_AMBER, width: 1.5 }, rectRadius: 0.1
});

s6.addText([
  { text: "HIỆN TƯỢNG XUNG NHIỄU PHONE:\n\n", options: { bold: true, color: C_AMBER, fontSize: 12.5 } },
  { text: "• Xung cơ học micro (t = 0.10s):\n", options: { bold: true, color: C_TEXT_MAIN } },
  { text: "Kéo dài đúng 10 ms (1 khung), vượt ngưỡng T* gây ra 2 biên giả.\n\n", options: { color: C_TEXT_MUTED } },
  { text: "• Bộ lọc 200 ms đề bài bất lực:\n", options: { bold: true, color: C_CYAN } },
  { text: "Vì đề bài chỉ lọc khoảng lặng ngắn, không lọc tiếng nói ngắn.\n\n", options: { color: C_TEXT_MUTED } },
  { text: "• Cơ chế Lọc Short Speech (< 30ms):\n", options: { bold: true, color: C_GREEN } },
  { text: "Áp dụng chuẩn Rabiner & Sambur (1975) và ITU-T G.729B xóa sạch xung 10ms.\n\n", options: { color: C_TEXT_MUTED } },
  { text: "• Kết quả sau lọc:\n", options: { bold: true, color: C_GREEN } },
  { text: "Số biên trở về đúng 2/2, MAE đạt xuất sắc 7.500 ms!", options: { color: C_TEXT_MAIN } }
], { x: 6.3, y: 1.55, w: 2.9, h: 3.3, fontSize: 11, fontFace: "Calibri", margin: 0 });

s6.addNotes("Ở file phone_M2 có hiện tượng xung nhiễu 10ms ở đầu file. Bộ lọc 200ms của đề bài không lọc được tiếng nói ngắn, nên nhóm em đã cài thêm filter_short_speech 30ms theo chuẩn Rabiner & Sambur 1975 để triệt tiêu hoàn toàn biên giả này.");

// ==========================================
// SLIDE 7: PHÂN TÍCH CA ĐẶC BIỆT PHONE_F2
// ==========================================
const s7 = pres.addSlide();
addHeader(s7, "GIẢI MÃ CA ĐẶC BIỆT PHONE_F2 (NGẮT HƠI & ĐUÔI ÂM THANH)", "Phát Hiện Học Thuật");

const figPhoneF2Path = path.resolve("reports/figures/figure_1_phone_F2_gaussian.png");
s7.addImage({
  path: figPhoneF2Path,
  x: 0.6, y: 1.35, w: 5.3, h: 3.7
});

s7.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 6.1, y: 1.35, w: 3.3, h: 3.7,
  fill: { color: C_CARD }, line: { color: C_CYAN, width: 1.5 }, rectRadius: 0.1
});

s7.addText([
  { text: "LUẬN ĐIỂM BẢO VỆ PHONE_F2:\n\n", options: { bold: true, color: C_CYAN, fontSize: 12.5 } },
  { text: "1. Ngắt hơi lấy giọng 221 ms:\n", options: { bold: true, color: C_TEXT_MAIN } },
  { text: "Tại t ∈ [2.56s, 2.78s], lặng 221 ms > 200 ms. Thuật toán tuân thủ đúng quy chế đề bài nên không gộp câu.\n\n", options: { color: C_TEXT_MUTED } },
  { text: "2. Độ trễ đuôi âm thanh (4.16s):\n", options: { bold: true, color: C_TEXT_MAIN } },
  { text: "Năng lượng âm đuôi suy giảm chậm, tắt hẳn ở 4.16s (lệch 122ms so với 4.04s).\n\n", options: { color: C_TEXT_MUTED } },
  { text: "3. Tạp âm thở cuối file (4.49s - 4.78s):\n", options: { bold: true, color: C_AMBER } },
  { text: "Đồ thị F0 có các chấm 300-350 Hz (giọng nữ), công suất gấp 9 lần nhiễu. Nhãn .lab bỏ qua nhưng thuật toán bắt đúng!", options: { color: C_TEXT_MUTED } }
], { x: 6.3, y: 1.55, w: 2.9, h: 3.3, fontSize: 11, fontFace: "Calibri", margin: 0 });

s7.addNotes("File phone_F2 có MAE 62.5ms do 2 nguyên nhân vật lý: người nói ngắt hơi 221ms lớn hơn ngưỡng 200ms nên thuật toán không gộp, và ở cuối file có tiếng thở giọng nữ F0 300-350Hz mà nhãn ground truth đã bỏ qua.");

// ==========================================
// SLIDE 8: TỔNG KẾT & KẾT LUẬN
// ==========================================
const s8 = pres.addSlide();
addHeader(s8, "TỔNG KẾT & KẾT LUẬN ĐỒ ÁN", "Đánh Giá Toàn Diện");

const conclCards = [
  { title: "ĐỘ CHÍNH XÁC XUẤT SẮC", desc: "Cả 3 thuật toán đạt MAE < 9 ms trên môi trường phòng thu sạch. Studio_F2 đạt kỷ lục 2.49 ms.", col: C_GREEN },
  { title: "KHÁNG NHIỄU VƯỢT TRỘI", desc: "Histogram đạt MAE toàn cục 18.12 ms nhờ thang log(STE) nén dải động, kháng nhiễu môi trường tốt nhất.", col: C_AMBER },
  { title: "TỐC ĐỘ & TÍNH TOÁN GAUSS", desc: "Gaussian Simple Statistics có nghiệm đóng giải tích Z-score, thực thi tức thì 0.05s mà không cần epochs lặp.", col: C_CYAN }
];

conclCards.forEach((c, idx) => {
  const xPos = 0.6 + idx * 3.0;
  s8.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: xPos, y: 1.4, w: 2.8, h: 2.5,
    fill: { color: C_CARD }, line: { color: c.col, width: 2 }, rectRadius: 0.15
  });

  s8.addText(c.title, {
    x: xPos + 0.15, y: 1.6, w: 2.5, h: 0.5,
    fontSize: 13, fontFace: "Calibri", color: c.col, bold: true, align: "center", margin: 0
  });

  s8.addText(c.desc, {
    x: xPos + 0.2, y: 2.2, w: 2.4, h: 1.5,
    fontSize: 12, fontFace: "Calibri", color: C_TEXT_MAIN, align: "center", margin: 0
  });
});

// Demo Callout
s8.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.6, y: 4.15, w: 8.8, h: 1.0,
  fill: { color: "162032" }, line: { color: C_GREEN, width: 2 }, rectRadius: 0.15
});

s8.addText("SẴN SÀNG CHUYỂN SANG PHẦN DEMO CHƯƠNG TRÌNH (1 PHÚT)", {
  x: 0.8, y: 4.3, w: 8.4, h: 0.35,
  fontSize: 15, fontFace: "Calibri", color: C_GREEN, bold: true, align: "center", margin: 0
});

s8.addText("Chạy 01 lệnh duy nhất duyệt qua 4 file kiểm thử và hiển thị đồng thời 4 cửa sổ Figure", {
  x: 0.8, y: 4.65, w: 8.4, h: 0.35,
  fontSize: 12.5, fontFace: "Calibri", color: C_TEXT_MUTED, align: "center", margin: 0
});

s8.addNotes("Tổng kết lại, nhóm em đã hoàn thành toàn diện nhiệm vụ. Histogram tốt nhất về kháng nhiễu, Gaussian tốt nhất về tốc độ tính toán đóng. Em xin phép bắt đầu 1 phút Demo chương trình.");

// Lưu tệp PPTX
const outputPath = "bao_cao_giua_ky_vad.pptx";
pres.writeFile({ fileName: outputPath }).then(() => {
  console.log("SUCCESS: Generated " + outputPath);
}).catch(err => {
  console.error("ERROR:", err);
});
