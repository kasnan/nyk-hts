import pickle

def load_txt():
    with open('data.pickle', 'rb') as file:
        data_list = []
        while True:
            try:
                data = pickle.load(file)
            except :
                break
            data_list.append(data)
        return data_list
        
def add_to_txt(item):
    f = open('data.pickle', 'ab')
    pickle.dump(item, f)
    f.close()

def update(items):
    with open('data.pickle', 'wb') as f:
        for item in items:
            pickle.dump(item, f, pickle.HIGHEST_PROTOCOL)
