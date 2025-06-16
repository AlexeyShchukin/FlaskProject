user = User(...) # Transient (объект ещё не связан с сессией)

session.add(user) # Pending

session.commit() # Persistent

session.close() # Detached v1
session.expunge() # Detached v2 (объект отвязан от сессии, сессия открыта)


user = User.query.get(id=1)
user.delete()
session.commit() # Deleted