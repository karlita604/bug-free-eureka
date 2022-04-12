import tenseal as ts

context = ts.context(ts.SCHEME_TYPE.BFV, poly_modulus_degree=4096, plain_modulus=1032193)
context

public_context = ts.context(ts.SCHEME_TYPE.BFV, poly_modulus_degree=4096, plain_modulus=1032193)
print("Is the context private?", ("Yes" if public_context.is_private() else "No"))
print("Is the context public?", ("Yes" if public_context.is_public() else "No"))

sk = public_context.secret_key()

# the context will drop the secret-key at this point
public_context.make_context_public()
print("Secret-key dropped")
print("Is the context private?", ("Yes" if public_context.is_private() else "No"))
print("Is the context public?", ("Yes" if public_context.is_public() else "No"))

'''
PART 2: 
Encryption and Evaluation
The next step after creating our TenSEALContext is to start doing some encrypted computation.
First, we create an encrypted vector of integers.
'''

plain_vector = [60, 66, 73, 81, 90]
encrypted_vector = ts.bfv_vector(context, plain_vector)
print("We just encrypted our plaintext vector of size:", encrypted_vector.size())
encrypted_vector

add_result = encrypted_vector + [1, 2, 3, 4, 5]
print(add_result.decrypt())

sub_result = encrypted_vector - [1, 2, 3, 4, 5]
print(sub_result.decrypt())

mul_result = encrypted_vector * [1, 2, 3, 4, 5]
print(mul_result.decrypt())

encrypted_add = add_result + sub_result
print(encrypted_add.decrypt())

encrypted_sub = encrypted_add - encrypted_vector
print(encrypted_sub.decrypt())

encrypted_mul = encrypted_add * encrypted_sub
print(encrypted_mul.decrypt())

'''
PART 3:
COMPARE COMPUTATION TIME ON ciphertext to 
plaintext (c2p) and ciphertext to ciphertext (c2c) evaluations (add, sub and mul).
'''

from time import time

t_start = time()
_ = encrypted_add * encrypted_mul
t_end = time()
print("c2c multiply time: {} ms".format((t_end - t_start) * 1000))

t_start = time()
_ = encrypted_add * [1, 2, 3, 4, 5]
t_end = time()
print("c2p multiply time: {} ms".format((t_end - t_start) * 1000))



# this should throw an error as the global_scale isn't defined yet
try:
    print("global_scale:", context.global_scale)
except ValueError:
    print("The global_scale isn't defined yet")

# you can define it to 2 ** 20 for instance
context.global_scale = 2 ** 20
print("global_scale:", context.global_scale)