package Models;

class Conversation {
	Project project;
	RegisteredUser[] participants;
	Date created;
	boolean isActive;

	Message[] messages;

	Message post(Message message) {
		return message;
	}

	boolean remove(Message message) {
		return false;
	}

	boolean close() {
		return false;
	}

}