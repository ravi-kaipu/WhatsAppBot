# WhatsAppBot
WhatsAppBot is a chatbot designed to answer unread messages in WhatsApp when owner is busy for some time.
At this moment, chat is designed to get set of question and answers stored in json (training_set.json) file and Q&A are very limited.

see raw text for perfect diagram ;)

Contact1 --> Unread messages \                                      / chatbot thread for Contact1 
Contact2 --> Unread messages  --> chatbot checks and waits to react --> chatbot thread for Contact2
Contact3 --> Unread messages /                                      \ chatbot thread for Contact3

TODO: Need to implement NPLK facebook/google to answer the questions preciously
