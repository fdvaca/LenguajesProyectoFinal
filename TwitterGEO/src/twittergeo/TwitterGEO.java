/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package twittergeo;

import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import twitter4j.Paging;
import twitter4j.Status;
import twitter4j.TwitterException;
import twitter4j.TwitterFactory;
import twitter4j.conf.ConfigurationBuilder;

/**
 *
 * @author Fernando
 */
public class TwitterGEO {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        setUpTwitter();
        
        
        
    }
    
    private static void setUpTwitter(){
        try {
            ConfigurationBuilder cb= new ConfigurationBuilder();
            cb.setDebugEnabled(true)
                    .setOAuthConsumerKey("2halIYtHPBYgpDzeEyjt9rRyz")
                    .setOAuthConsumerSecret("nFpZtU0UfxDzUZI6kxV27m1ykdwg3ARGtbeDasSpw1q5YR1NlJ")
                    .setOAuthAccessToken("3418827076-s1ZPyH4wvD7R5dn1WPy3GpLCAOpBUHfH4fkQOMf")
                    .setOAuthAccessTokenSecret("u32pEwjgtCCpCuwFLm4a7uazyXPw85fr2gVxey3PBXUdu");
            
            TwitterFactory tf=new TwitterFactory(cb.build());
            twitter4j.Twitter twitter=tf.getInstance();
            Paging p=new Paging();
            p.setCount(200);
            List<Status> status=twitter.getUserTimeline("@IGecuador",p);
            
            
            int count=0;
            for(Status st:status){
                System.out.println(st.getUser().getName()+"-------"+st.getText()+"\n");
                count++;
            }
            System.out.println(count);
        } catch (TwitterException ex) {
            Logger.getLogger(TwitterGEO.class.getName()).log(Level.SEVERE, null, ex);
        }
        
    }
    
}
