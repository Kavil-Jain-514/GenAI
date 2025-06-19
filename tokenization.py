import tiktoken
# import abcd

encoder = tiktoken.encoding_for_model('gpt-4o')
print("Vocab Size", encoder.n_vocab) #200,019

#Encode
text = "The cat sat on the mat"
tokens = encoder.encode(text)
print("Tokens", tokens) #[976, 9059, 10139, 402, 290, 2450]

#Decode
myTokens = [976, 9059, 10139, 402, 290, 2450]
decode = encoder.decode(myTokens)
print("Decoded", decode) #The cat sat on the mat

# xyz = abcd.xyz()