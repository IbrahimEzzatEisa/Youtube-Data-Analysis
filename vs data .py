import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


youtube_data = pd.read_csv("video_result.csv")

print(youtube_data.corr())
plt.scatter(youtube_data.viewCount , youtube_data.likeCount,
          youtube_data.dislikeCount , youtube_data.commentCount  ,youtube_data.subscribeCount  )
plt.show()












