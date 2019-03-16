import json
import cv2

with open('sample_img\out\input_file4.json') as f:
    data = json.load(f)

max_confidence = 0;
second_max_confidence = 0;

for item in data:
    if item["label"] == "person":
	    if ((item["bottomright"]["x"] - item["topleft"]["x"]) * (item["bottomright"]["y"] - item["topleft"]["y"])) > max_confidence:
		    best_result = item
		    max_confidence = ((item["bottomright"]["x"] - item["topleft"]["x"]) * (item["bottomright"]["y"] - item["topleft"]["y"]))

for item in data:
    if item["label"] == "person":
	    if (((item["bottomright"]["x"] - item["topleft"]["x"]) * (item["bottomright"]["y"] - item["topleft"]["y"])) > second_max_confidence) and (item["topleft"] != best_result["topleft"]):
		    second_best_result = item
		    second_max_confidence = ((item["bottomright"]["x"] - item["topleft"]["x"]) * (item["bottomright"]["y"] - item["topleft"]["y"]))

img = cv2.imread('sample_img\input_file4.png')

y = best_result["topleft"]["y"];
y1 = best_result["bottomright"]["y"];
h1 = y1 - y;

x01 = x = best_result["topleft"]["x"];
x1 = best_result["bottomright"]["x"];
w1 = x1 - x;

crop_img1 = img[y:y+h1, x:x+w1]

y = second_best_result["topleft"]["y"];
y1 = second_best_result["bottomright"]["y"];
h2 = y1 - y;

x02 = x = second_best_result["topleft"]["x"];
x1 = second_best_result["bottomright"]["x"];
w2 = x1 - x;

crop_img2 = img[y:y+h2, x:x+w2]


##left or right
if ((x01 + x01 + w1)/2) > ((x02 + x02 + w2)/2):
    best_result["left"] = False
    second_best_result["left"] = True
else:
    best_result["left"] = True
    second_best_result["left"] = False
	
##stance
ratio1 = (best_result["bottomright"]["y"] - best_result["topleft"]["y"]) / (best_result["bottomright"]["x"] - best_result["topleft"]["x"])
ratio2 = (second_best_result["bottomright"]["y"] - second_best_result["topleft"]["y"]) / (second_best_result["bottomright"]["x"] - second_best_result["topleft"]["x"])

if best_result["bottomright"]["y"] - second_best_result["bottomright"]["y"] < -30:
    best_result["stance"] = "jump"
    if(second_best_result["bottomright"]["x"] - second_best_result["topleft"]["x"] < 200) and (ratio2 < 1.3):
        second_best_result["stance"] = "crouch"
    else:
        second_best_result["stance"] = "stand"	
elif second_best_result["bottomright"]["y"] - best_result["bottomright"]["y"] < -30:
    second_best_result["stance"] = "jump"
    if(best_result["bottomright"]["x"] - best_result["topleft"]["x"] < 200) and (ratio1 < 1.3):
        best_result["stance"] = "crouch"
    else:
        best_result["stance"] = "stand"
else:
    if (best_result["bottomright"]["x"] - best_result["topleft"]["x"] < 200) and (ratio1 < 1.3):
        best_result["stance"] = "crouch"
    else:
        best_result["stance"] = "stand"
    if (second_best_result["bottomright"]["x"] - second_best_result["topleft"]["x"] < 200) and (ratio2 < 1.3):
        second_best_result["stance"] = "crouch"
    else:
        second_best_result["stance"] = "stand"
		
##color
avg1 = [0,0,0]
avg2 = [0,0,0]

blue1 = 0;
blue2 = 0;

for i in range(h1):
    for j in range(w1):
        avg1 += crop_img1[i-1][j-1]

avg1[0] /= h1*w1;
avg1[1] /= h1*w1;
avg1[2] /= h1*w1;
			
for i in range(h2):
    for j in range(w2):
        avg2 += crop_img2[i-1][j-1]

avg2[0] /= h2*w2;
avg2[1] /= h2*w2;
avg2[2] /= h2*w2;

diff1 = avg1[0] - avg1[1] + avg1[0] - avg1[2];
diff2 = avg2[0] - avg2[1] + avg2[0] - avg2[2];
if(diff1 > diff2):
    blue_player = best_result
    blue_player["label"] = "blue"
    yellow_player = second_best_result
    yellow_player["label"] = "yellow"
else:
    blue_player = second_best_result
    blue_player["label"] = "blue"
    yellow_player = best_result
    yellow_player["label"] = "yellow"

print({"distance": abs(((x01 + x01 + w1)/2) - ((x02 + x02 + w2)/2)) })
print(blue_player)
print(yellow_player)	

cv2.imshow("cropped1", crop_img1)
cv2.imshow("cropped2", crop_img2)
cv2.waitKey(0)
