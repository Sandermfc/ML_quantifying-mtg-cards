import tensorflow as tf
import random
import unicodecsv as csv

#import csv file
def separateInputs():
	random.seed()
	with open("input.csv", "r") as inputfile:
		with open("learningData.csv", "w") as learning:
			with open("validationData.csv", "w") as validation:
				with open("testData.csv", "w") as test:
					reader = csv.reader(inputfile,delimiter = ",")
					writerl = csv.writer(learning, quotechar = "'", quoting=csv.QUOTE_ALL)
					writerv = csv.writer(validation, quotechar = "'", quoting=csv.QUOTE_ALL)
					writert = csv.writer(test, quotechar = "'", quoting=csv.QUOTE_ALL)
					data = list(reader)
					for row in data:
						a = random.randint(0,9)
						if(a < 6):
							writerl.writerow(row)
						elif(a > 5 and a < 8):
							writerv.writerow(row)
						elif(a > 7 and a < 10):
							writert.writerow(row)


#change the description to value

#change keyword to value

#change rarity to value


#training TODO
def run_training(train_X, train_Y):
    X = tf.placeholder(tf.float32, [m, n])
    Y = tf.placeholder(tf.float32, [m, 1])

    # weights
    W = tf.Variable(tf.zeros([n, 1], dtype=np.float32), name="weight")
    b = tf.Variable(tf.zeros([1], dtype=np.float32), name="bias")

    # linear model
    activation = tf.add(tf.matmul(X, W), b)
    cost = tf.reduce_sum(tf.square(activation - Y)) / (2*m)
    optimizer = tf.train.GradientDescentOptimizer(FLAGS.learning_rate).minimize(cost)

    with tf.Session() as sess:
        init = tf.initialize_all_variables()
        sess.run(init)

        for step in range(FLAGS.max_steps):

            sess.run(optimizer, feed_dict={X: np.asarray(train_X), Y: np.asarray(train_Y)})

            if step % FLAGS.display_step == 0:
                print "Step:", "%04d" % (step+1), "Cost=", "{:.2f}".format(sess.run(cost, \
                    feed_dict={X: np.asarray(train_X), Y: np.asarray(train_Y)})), "W=", sess.run(W), "b=", sess.run(b)

        print "Optimization Finished!"
        training_cost = sess.run(cost, feed_dict={X: np.asarray(train_X), Y: np.asarray(train_Y)})
        print "Training Cost=", training_cost, "W=", sess.run(W), "b=", sess.run(b), '\n'

        print "Predict.... (Predict a house with 1650 square feet and 3 bedrooms.)"
        predict_X = np.array([1650, 3], dtype=np.float32).reshape((1, 2))

        # Do not forget to normalize your features when you make this prediction
        predict_X = predict_X / np.linalg.norm(predict_X)

        predict_Y = tf.add(tf.matmul(predict_X, W),b)
        print "House price(Y) =", sess.run(predict_Y)

def feature_normalize(train_X):

    global mean, std
    mean = np.mean(train_X, axis=0)
    std = np.std(train_X, axis=0)

    return (train_X - mean) / std2


def main():
	separateInputs()
	print("main")


if __name__ == "__main__":
	main();
