import thulac
import pandas as pd


df = pd.read_csv('电影详细信息.csv')
story_brief_list = [df['剧情简介'][i].replace('\n', '').replace('\u3000', '').strip(' ') for i in range(df['剧情简介'].shape[0])]
thu1 = thulac.thulac(filt=True, rm_space=True)

token_freq_dict = dict()
for story in story_brief_list:
    token_entity_dict = thu1.cut(story, text=False)
    for key, value in token_entity_dict:
        if len(key) > 1:
            if key in token_freq_dict.keys():
                token_freq_dict[key] += 1
            else:
                token_freq_dict[key] = 1

token_freq_dict_order = sorted(token_freq_dict.items(), key=lambda x: x[1], reverse=True)
token_list = []
freq_list = []
for (token, freq) in token_freq_dict_order:
    token_list.append(token)
    freq_list.append(freq)
data_frame = pd.DataFrame({'分词': token_list, '出现次数': freq_list})
data_frame.to_csv('token_freq.csv')

