package Models;

public class RegisteredUser {
	String name;
	String displayName;
	String email;
	Profile[] profiles;
	Conversation[] conversations;
	public boolean setPassword(String pass) {
		return false;
	}
}