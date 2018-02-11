import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.zip.GZIPInputStream;
import java.util.zip.GZIPOutputStream;

import gnu.trove.map.hash.TObjectIntHashMap;
import gnu.trove.map.hash.TIntObjectHashMap;

public class Dictionary {
    public TObjectIntHashMap<String> word2id;
    public TIntObjectHashMap<String> id2word;

    //--------------------------------------------------
    // constructors
    //--------------------------------------------------

    public Dictionary(){
        word2id = new TObjectIntHashMap<String>();
        id2word = new TIntObjectHashMap<String>();
    }

    //---------------------------------------------------
    // get/set methods
    //---------------------------------------------------

    public String getWord(int id){
        return id2word.get(id);
    }

    public int getID(String word){
        return word2id.get(word);
    }

    //----------------------------------------------------
    // checking methods
    //----------------------------------------------------
    /**
     * check if this dictionary contains a specified word
     */
    public boolean contains(String word){
        return word2id.containsKey(word);
    }

    public boolean contains(int id){
        return id2word.containsKey(id);
    }
    //---------------------------------------------------
    // manupulating methods
    //---------------------------------------------------
    /**
     * add a word into this dictionary
     * return the corresponding id
     */
    public int addWord(String word){
        if (!contains(word)){
            int id = word2id.size();

            word2id.put(word, id);
            id2word.put(id,word);

            return id;
        }
        else return getID(word);		
    }

    //---------------------------------------------------
    // I/O methods
    //---------------------------------------------------
    /**
     * read dictionary from file
     */
    public boolean readWordMap(String wordMapFile)
    {
        try {
            BufferedReader reader = new BufferedReader(new InputStreamReader(
                        new GZIPInputStream(
                            new FileInputStream(wordMapFile)), "UTF-8"));
            String line;

            for (int i = 0; (line = reader.readLine()) != null; i++) {
                String word = line.trim();
                id2word.put(i, word);
                word2id.put(word, i);
            }

            reader.close();
            return true;
        }
        catch (Exception e) {
            System.out.println("Error while reading dictionary:" + e.getMessage());
            e.printStackTrace();
            return false;
        }		
    }

    public boolean writeWordMap(String wordMapFile)
    {
        try {
            BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(
                        new GZIPOutputStream(
                            new FileOutputStream(wordMapFile)), "UTF-8"));

            //write word to id
            for (int i = 0; i < id2word.size(); i++) {
                writer.write(id2word.get(i) + "\n");
            }

            writer.close();
            return true;
        }
        catch (Exception e) {
            System.out.println("Error while writing word map " + e.getMessage());
            e.printStackTrace();
            return false;
        }
    }
}
