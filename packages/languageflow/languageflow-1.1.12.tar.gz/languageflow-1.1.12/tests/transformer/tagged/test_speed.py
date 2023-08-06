from unittest import TestCase
import time
from languageflow.transformer.tagged import TaggedTransformer

text = "Đầu giờ chiều ngày 7/9, trao đổi với Báo Giao thông, ông Nguyễn Ngọc Hùng, Giám đốc Sở Thông tin và Truyền thông tỉnh Gia Lai cho biết đã đọc thông tin trên Báo Gia Lai. Thông tin khá mù mờ nhưng rất được người dân quan tâm, ông Hùng nói và cho biết hôm nay họp cả ngày nên chưa kịp yêu cầu Báo Gia Lai báo cáo. Trước đó, báo điện tử Gia Lai đã đăng tải bài báo Một công dân Gia Lai khẳng định phát hiện địa điểm máy bay MH370 rơi. Bài báo thông tin: 4 năm trước, người đàn ông này lúc ấy đang làm ăn tại Đắk Nông trong lúc tình cờ tìm kiếm thông tin hình ảnh vệ tinh trên mạng bỗng thấy một chiếc máy bay có kích thước giống chiếc máy bay MH370 rơi trong một lòng hồ. Sau đó, anh đã quay lại hình ảnh và vị trí chiếc máy bay này trên Google Earth. Hiện nay, lòng hồ mực nước dâng cao, không thể quan sát bằng mắt thường nếu đi trên mặt hồ hoặc chụp ảnh qua vệ tinh. Người này sau đó đã đưa clip lên YouTube, đến nay có hơn 5.700 lượt xem (Tuy nhiên, vì nhiều lý do nên đã được gỡ xuống) nhưng không ai ý kiến gì. Gần đây qua báo chí anh thấy một người Anh đưa thông tin đã phát hiện được máy bay MH370 tại rừng rậm Campuchia. Qua hình ảnh, anh nhận thấy clip của họ giống clip của anh nhưng có dấu hiệu chỉnh sửa hình ảnh máy bay trong clip mà anh đưa lên mạng cách đây 4 năm, vậy nên anh quyết định công bố thông tin này cho báo điện tử Gia Lai. Cũng theo báo điện tử Gia Lai, chiếc máy bay được người này phát hiện đo được độ dài khoảng 60,78m, sải cánh 31,23m, máy bay còn nguyên vẹn, không bị vỡ, đầu cắm xuống lòng hồ. Kích thước này tương đồng với thông tin về chiếc máy bay MH370 của Hãng Hàng không Malaysia. Chiếc máy bay này rơi xuống nước ở độ sâu khoảng 30m và nhiều khả năng ngập dưới bùn 5-6m, chứ không phải nằm trong rừng rậm và không thuộc địa phận Campuchia. Qua hình ảnh có thể thấy cánh chiếc máy bay méo mó, không nhìn rõ, chứng tỏ có thể trước khi rơi, máy bay va chạm nhẹ vào cây rừng hoặc bị ngập sâu dưới bùn đất. Anh này thậm chí còn khẳng định chỉ cần 2-3 ngày là tìm thấy chính xác vị trí chiếc máy bay MH370. Nếu Chính phủ Malaysia đồng ý anh sẽ xin phép các cơ quan chức năng thuê thợ lặn tìm kiếm. Việc tìm kiếm này nếu không đúng thì hãng hàng không Malaysia cũng không mất gì, toàn bộ chi phí người này sẽ chịu." * 4

template = [
    "T[-2].lower", "T[-1].lower", "T[0].lower", "T[1].lower", "T[2].lower",

    "T[-1].isdigit", "T[0].isdigit", "T[1].isdigit",

    "T[-1].istitle", "T[0].istitle", "T[1].istitle",
    "T[0,1].istitle", "T[0,2].istitle",

    "T[-2].is_in_dict", "T[-1].is_in_dict", "T[0].is_in_dict", "T[1].is_in_dict", "T[2].is_in_dict",
    "T[-2,-1].is_in_dict", "T[-1,0].is_in_dict", "T[0,1].is_in_dict", "T[1,2].is_in_dict",
    "T[-2,0].is_in_dict", "T[-1,1].is_in_dict", "T[0,2].is_in_dict",

    # word unigram and bigram and trigram
    "T[-2]", "T[-1]", "T[0]", "T[1]", "T[2]",
    "T[-2,-1]", "T[-1,0]", "T[0,1]", "T[1,2]",
    "T[-2,0]", "T[-1,1]", "T[0,2]",
]

# Speed
#  =======================================================
# | sentences  | version           | speed                |
#  =======================================================
# | 4          | pyvi              | 0.0546               |
# | 4          | v1.1.8a1          | 18.564               |
# | 8          | pyvi              | 0.1139               |
# | 16         | pyvi              | 0.2418               |
#  =======================================================

class TestSpeed(TestCase):
    def test_speed(self):
        start = time.time()
        tokens = text.split()
        tokens = [(token,) for token in tokens]
        transformer = TaggedTransformer(template)
        x2 = transformer.transform([tokens])
        end = time.time()
        duration = end - start
        self.assertLess(duration, 3)





