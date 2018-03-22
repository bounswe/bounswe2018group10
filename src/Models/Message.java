package Models;

class Message {
	RegisteredUser sender;
	RegisteredUser recipient;
	Date created;
	String body;
	File[] files;
	Message repliedTo;

	Message postTo(Conversation conversation) {
		return null;
	}

	boolean delete() {
		return true;
	}
}M