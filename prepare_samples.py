import pymysql.cursors

skip = False
samples = []
labels = []

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='small_rekomendacyjny')
cur = conn.cursor()
cur.execute("SELECT * FROM help ORDER BY RAND() LIMIT 1000")

for row in cur:
    cur_movie = conn.cursor()
    cur_movie.execute("SELECT * FROM movie WHERE id = %s", row[1])
    movie = cur_movie.fetchone()
    movie_rating = movie[2]
    genre_ratings = []
    print(movie)
    cur_genres = conn.cursor()
    cur_genres.execute("SELECT * FROM movie_genre WHERE movie_id = %s", movie[0])
    # for genre in cur_genres:


        #     foreach($movie->genres as $genre) {
        #         $ratingModel = Rating::find()->where(['user_id' => $help->user_id])->andWhere(['genre_id' => $genre->id])->one();
        #         if($ratingModel) {
        #             $rating = $ratingModel->rating;
        #             $genre_ratings[] = $rating;
        #         } else {
        #             $skip = true;
        #             break;
        #         }
        #     }
        #     if(!$skip) {
        #         $genre_rating = Average::median($genre_ratings);
        #         $samples[] = [$help->rating, $movie_rating, $genre_rating];
        #         $labels[] = $help->rating;
        #     }
        #     $skip = false;
        # }
        # $path = Yii::getAlias('@console') . '/files';
        # $fileName = '/train.txt';
        # $file = fopen($path . $fileName, 'wb');
        # foreach($samples as $sample)
        # {
        #     foreach($sample as $data) {
        #         fwrite($file, $data . '; ');
        #     }
        #     fwrite($file, PHP_EOL);
        # }
        # fclose($file);
        #
        # $fileName = '/labels.txt';
        # $file = fopen($path . $fileName, 'wb');
        # foreach($labels as $label)
        # {
        #         fwrite($file, $label . PHP_EOL);
        # }
        # fclose($file);
        # return [
        #     'samples' => $samples,
        #     'labels' => $labels
        #     ];
