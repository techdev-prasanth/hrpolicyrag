from tasks import add,run


print("File has been strated .......")
result = add.delay(2, 3)

print(result.id)
print(result.get())
print("add func called",result)

mrun = run.delay()

print(mrun)
print("mrun func called",mrun)
