import inferpy as inf
import numpy as np
import tensorflow as tf


@inf.probmodel
def pca(k,d):
    w = inf.Normal(loc=np.zeros([k,d]), scale=1, name="w")      # shape = [k,d]
    with inf.datamodel():
        z = inf.Normal(np.ones([k]),1, name="z")                # shape = [N,k]
        x = inf.Normal(z @ w , 1, name="x")                     # shape = [N,d]






#### data (do not show)
# generate training data
N = 1000
sess = tf.Session()
x_train = np.concatenate([inf.Normal([0.0,0.0], scale=1.).sample(int(N/2)), inf.Normal([10.0,10.0], scale=1.).sample(int(N/2))])



### encapsulated inference

#28


@inf.probmodel
def qmodel(k,d):
    qw_loc = inf.Parameter(tf.ones([k,d]), name="qw_loc")
    qw_scale = tf.math.softplus(inf.Parameter(tf.ones([k, d]), name="qw_scale"))
    qw = inf.Normal(qw_loc, qw_scale, name="w")

    with inf.datamodel():
        qz_loc = inf.Parameter(tf.ones([k]), name="qz_loc")
        qz_scale = tf.math.softplus(inf.Parameter(tf.ones([k]), name="qz_scale"))
        qz = inf.Normal(qz_loc, qz_scale, name="z")



# set the inference algorithm
VI = inf.inference.VI(qmodel(k=1,d=2), epochs=1000)
# create an instance of the model
m = pca(k=1,d=2)
# run the inference
m.fit({"x": x_train}, VI)

"""
 0 epochs	 44601.14453125....................
 200 epochs	 44196.98046875....................
 400 epochs	 50616.359375....................
 600 epochs	 41085.6484375....................
 800 epochs	 30349.79296875....................
 
"""

print(m.posterior['w'].sample())


"""
>>> m.posterior['w']
<inf.RandomVariable (Normal distribution) named w_2/, shape=(1, 2), dtype=float32>

"""


# 70


## ELBO definition

from tensorflow_probability import edward2 as ed

# define custom elbo function
def custom_elbo(pmodel, qmodel, sample_dict):
    # create combined model
    plate_size = pmodel._get_plate_size(sample_dict)

    # expand the qmodel (just in case the q model uses data from sample_dict, use interceptor too)
    with ed.interception(inf.util.interceptor.set_values(**sample_dict)):
        qvars, _ = qmodel.expand_model(plate_size)

    # expand de pmodel, using the intercept.set_values function, to include the sample_dict and the expanded qvars
    with ed.interception(inf.util.interceptor.set_values(**{**qvars, **sample_dict})):
        pvars, _ = pmodel.expand_model(plate_size)

    # compute energy
    energy = tf.reduce_sum([tf.reduce_sum(p.log_prob(p.value)) for p in pvars.values()])

    # compute entropy
    entropy = - tf.reduce_sum([tf.reduce_sum(q.log_prob(q.value)) for q in qvars.values()])

    # compute ELBO
    ELBO = energy + entropy

    # This function will be minimized. Return minus ELBO
    return -ELBO



# set the inference algorithm
VI = inf.inference.VI(qmodel(k=1,d=2), loss=custom_elbo, epochs=1000)

# run the inference
m.fit({"x": x_train}, VI)




##95


### optimization loop

# instance
q = qmodel(k=1,d=2)

# for not evaluating ELBO tensor
inf.util.runtime.set_tf_run(False)
# extract the computational graph of the ELBO
loss_tensor = inf.inference.loss_functions.elbo.ELBO(m,q, {"x": x_train})

# build an optimizer to minimize the ELBO
optimizer = tf.train.AdamOptimizer(learning_rate=0.1)
train = optimizer.minimize(loss_tensor)

# start a session
sess = tf.Session()
# intialize the TF variables
sess.run(tf.global_variables_initializer())



# optimization loop
t = []
for i in range(0,100):
    sess.run(train)
    t += [sess.run(loss_tensor)]
    print(t[-1])


# extract the posterior distributions
posterior_qvars = {name: qv.build_in_session(sess) for name, qv in q._last_expanded_vars.items()}





# 134
