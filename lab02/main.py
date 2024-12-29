from transformers import GPT2LMHeadModel, GPT2Tokenizer, AutoModelForCausalLM, AutoTokenizer


model_name_or_path = "rugpt3large_based_on_gpt2"

tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
model = GPT2LMHeadModel.from_pretrained(model_name_or_path)

# tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
# model = AutoModelForCausalLM.from_pretrained(model_name_or_path)

# text = '''Аннотация к КНИР длиной не более 150 слов и 
#     не более 10 предложений на тему Системынй анализ архитектур и 
#     функциональности основных СУБД, использующих модель данных ключ-значение звучит так:'''
# text = "Аннотация на тему системный анализ архитектур и функциональности основных СУБД, использующих модель данных ключ-значение звучит так: "
text = "Аннотация на тему системный анализ баз данных ключ-значение звучит так: "

# rugpt3large/small_based_on_gpt2
input_ids = tokenizer.encode(text, return_tensors="pt")
out = model.generate(
    input_ids,
    max_length=200
)

out = model.generate(input_ids, max_length=200)
generated_text = list(map(tokenizer.decode, out))[0]

# ruGPT-3.5-13B
# encoded_input = tokenizer(text, return_tensors='pt', add_special_tokens=False)
# out = model.generate(
#     **encoded_input,
#     num_beams=2,
#     do_sample=True,
#     max_new_tokens=150
# )
# generated_text = tokenizer.decode(out[0], skip_special_tokens=True)

# output
print(generated_text)