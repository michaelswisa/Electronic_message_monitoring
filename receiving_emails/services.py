from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def send_all_emails_to_mongo(email):
    producer.send('messages.all', value=email)
    print(f"Email sent to MongoDB: {email}")


def send_emails_hostage_to_postgres(email):
    producer.send('messages.hostage', value=email)
    print(f"Email sent to PostgreSQL: {email}")


def send_emails_explos_to_postgres(email):
    producer.send('messages.explos', value=email)
    print(f"Email sent to PostgreSQL: {email}")


def creating_explos_list(explos, hostage, the_rest):
    new_sentences = explos
    for sentence in hostage:
        if not sentence in new_sentences:
            new_sentences.append(sentence)
    for sentence in the_rest:
        if not sentence in new_sentences:
            new_sentences.append(sentence)
    return new_sentences


def creating_hostage_list(hostage, explos, the_rest):
    new_sentences = hostage
    for sentence in explos:
        if not sentence in new_sentences:
            new_sentences.append(sentence)
    for sentence in the_rest:
        if not sentence in new_sentences:
            new_sentences.append(sentence)
    return new_sentences


def find_hostage_and_explos_words(sentences):
    hostage_words = ['hostage', 'hostages']
    explos_words = ['explos', 'explosive', 'explosives']
    explos_sentences = []
    hostage_sentences = []
    sentences_without_words_suspicious = []

    for sentence in sentences:
        if any(word in sentence.lower() for word in hostage_words):
            hostage_sentences.append(sentence)
        if any(word in sentence.lower() for word in explos_words):
            explos_sentences.append(sentence)
        if not any(word in sentence.lower() for word in hostage_words + explos_words):
            sentences_without_words_suspicious.append(sentence)

    return explos_sentences, hostage_sentences, sentences_without_words_suspicious


def send_email_to_kafka(email):
    send_all_emails_to_mongo(email)

    explos, hostage, the_rest = find_hostage_and_explos_words(email['sentences'])

    if len(explos) > 0:
        list_for_explos = creating_explos_list(explos, hostage, the_rest)
        email['sentences'] = list_for_explos
        send_emails_explos_to_postgres(email)

    if len(hostage) > 0:
        list_for_hostage = creating_hostage_list(hostage, explos, the_rest)
        email['sentences'] = list_for_hostage
        send_emails_hostage_to_postgres(email)
