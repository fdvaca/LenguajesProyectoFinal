/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package twittergeo;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import twitter4j.Paging;
import twitter4j.Status;
import twitter4j.Twitter;
import twitter4j.TwitterException;
import twitter4j.TwitterFactory;
import twitter4j.conf.ConfigurationBuilder;

/**
 *
 * @author Vaca, Escobar, Palma
 */
public class TwitterGEO {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        setUpTwitter();
    }

    private static void setUpTwitter() {
        final String COMMA_DELIMITER = ",";
        final String NEW_LINE_SEPARATOR = "\n";
        final String FILE_HEADER = "id,url,fecha,contenido,cantidadRT,cantidadFAV,";

        int pageno = 1;
        String user = "@IGecuador";
        List<Status> statuses = new ArrayList();
        ConfigurationBuilder cb = new ConfigurationBuilder();

        cb.setDebugEnabled(
                true)
                .setOAuthConsumerKey("2halIYtHPBYgpDzeEyjt9rRyz")
                .setOAuthConsumerSecret("nFpZtU0UfxDzUZI6kxV27m1ykdwg3ARGtbeDasSpw1q5YR1NlJ")
                .setOAuthAccessToken("3418827076-s1ZPyH4wvD7R5dn1WPy3GpLCAOpBUHfH4fkQOMf")
                .setOAuthAccessTokenSecret("u32pEwjgtCCpCuwFLm4a7uazyXPw85fr2gVxey3PBXUdu");

        Twitter twitter = new TwitterFactory(cb.build()).getInstance();

        while (true) {
            try {
                int size = statuses.size();
                Paging page = new Paging(pageno++, 100);
                statuses.addAll(twitter.getUserTimeline(user, page));
                if (statuses.size() == size) {
                    break;
                }

            } catch (TwitterException e) {
                e.printStackTrace();
            }
        }

        FileWriter fileWriter = null;

        try {
            fileWriter = new FileWriter("tweetsIG.csv");
            fileWriter.append(FILE_HEADER);
            fileWriter.append(NEW_LINE_SEPARATOR);

            for (Status st : statuses) {
                fileWriter.append(String.valueOf(st.getId()));
                fileWriter.append(COMMA_DELIMITER);
                fileWriter.append(String.valueOf(st.getDisplayTextRangeEnd()));
                fileWriter.append(COMMA_DELIMITER);
                fileWriter.append(String.valueOf(st.getCreatedAt()));
                fileWriter.append(COMMA_DELIMITER);
                fileWriter.append(st.getText());
                fileWriter.append(COMMA_DELIMITER);
                fileWriter.append(String.valueOf(st.getRetweetCount()));
                fileWriter.append(COMMA_DELIMITER);
                fileWriter.append(String.valueOf(st.getFavoriteCount()));
                fileWriter.append(NEW_LINE_SEPARATOR);
            }
            System.out.println("csv created!!!");

        } catch (IOException e) {
            System.out.println("Error creating csv !!!");
        } finally {
            try {
                fileWriter.close();
            } catch (IOException e) {
                System.out.println("Error while closing fileWriter !!!");
            }
        }
    }

}
