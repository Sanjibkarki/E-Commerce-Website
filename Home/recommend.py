import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.apps import apps


class ContentRecommender:

    def __init__(self):
        self.vectorizer = None
        self.tfidf_matrix = None
        self.train_data = None

    def load_data(self):
        
        Product = apps.get_model("Home", "Product")

        qs = Product.objects.all().values(
            "uuid",
            "Name",
            "Description",
            "Image",
            "Price",
            "category"
        )
        df = pd.DataFrame(list(qs))
        df["Description"] = df["Description"].fillna("")
        self.train_data = df
        return df

    def train(self):

        if self.train_data is None:
            self.load_data()

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            min_df=1
        )

        self.tfidf_matrix = self.vectorizer.fit_transform(
            self.train_data["Description"]
        )

    def recommend(self, item_name, top_n=5):
        if self.vectorizer is None or self.tfidf_matrix is None:
            self.train()

        if item_name not in self.train_data["Name"].values:
            return pd.DataFrame()

        idx = self.train_data[self.train_data["Name"] == item_name].index[0]

        similarities = cosine_similarity(
            self.tfidf_matrix[idx],
            self.tfidf_matrix
        ).flatten()
        similar_indices = similarities.argsort()[::-1][1:top_n + 1]

        results = self.train_data.iloc[similar_indices][[
            "uuid",
            "Name",
            "Description",
            "Image",
            "Price",
            "category"
        ]]

        return results
