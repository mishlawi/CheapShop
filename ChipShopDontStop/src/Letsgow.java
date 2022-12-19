import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Letsgow {


//se os dois tiverem qtd e encontrar um numero nos 2 e forem diferentes manda logo false,
// se os 2 numeros forem iguais ou nao encotrar numero num deles pesquisa palavras em comum
    //barata mudou a função no cafe tropinha
    public static boolean podeSerOMesmo(Produto a , Produto b){
        //            Nome                               ,       MARCA      QUANTIDADE     PRECO            PPU          PROMO     EAN


        int conta=0;
        boolean pode=false;

        /*
        if(!a.getQuantidade().equals("NONE") && !a.getQuantidade().equals("z") && !a.getQuantidade().isEmpty() &&    !b.getQuantidade().equals("NONE") && !b.getQuantidade().equals("z") && !b.getQuantidade().isEmpty()       ){
            String regexQTD = "\\d+";
            Pattern p = Pattern.compile(regexQTD);
            Matcher ma = p.matcher(a.getQuantidade());
            Matcher mb = p.matcher(b.getQuantidade());

            boolean resa = ma.find();
            boolean resb = mb.find();

            if(resa && resb){
                String qtd_a = ma.group();
                String qtd_b = mb.group();

                int qtd_a_int=Integer.parseInt(qtd_a);
                int qtd_b_int=Integer.parseInt(qtd_b);


                //       ! qtd_a.equals(qtd_b)
                if (     qtd_a_int!=qtd_b_int && qtd_a_int!=(qtd_b_int*10)&& qtd_a_int!=(qtd_b_int*100) && qtd_a_int!=(qtd_b_int/10) && qtd_a_int!=(qtd_b_int/100)     )
                    return false;

            }
        }

         */
        String baratata = a.getQuantidade().toLowerCase();
        baratata=  baratata.replace(" ","");

        String baratata2 = b.getQuantidade().toLowerCase();
        baratata2=  baratata2.replace(" ","");

        if(!baratata.equals(baratata2))
            return false;


            String[] auxB=b.getNome().split(" ");


            for (String aa : auxB){
                if(a.getNome().contains(aa) && !aa.equals(a.getMarca() )  && !aa.equals("DE") &&  !aa.equals("PARA") && !aa.equals("COM") && !aa.equals("SEM")  && !aa.equals("A") && !aa.equals("E") && !aa.equals("I") && !aa.equals("O") && !aa.equals("U")  && !aa.equals("OU")                    )
                    conta++;
            }

            double graudecerteza=0.5;


            if(conta>graudecerteza* auxB.length )
                pode=true;



        return pode;
    }



    public static void main(String[] args){
        int kappa=0;

        //1oCSV TEM QUE TER EAN
        String _1oCSV="auchan.csv";
        String _2oCSV="ProdutosPingoDoce.csv";



        Map<String,List<Produto>> auchanMap = new HashMap<>();
        Map<String,List<Produto>> secondMap = new HashMap<>();

        Map<String,Produto> auchanMapEAN = new HashMap<>();

        int qts=0;
        int i,j=0;


        //LER OS DO AUCHAN E POR EM DOIS HASMAPS: 1 - O HASHMAP DO AUCHAN POR MARCA | 2 - O hasmpap DO AUCHAN MAS POR EAN
        try {
            String path_1oCSV="./"+_1oCSV;
            File myObj = new File(path_1oCSV);
            Scanner myReader = new Scanner(myObj);
            String data = myReader.nextLine();
            while (myReader.hasNextLine()) {
                 data = myReader.nextLine();
                String copy = data.toUpperCase();
                String aux[] = copy.split(",");


                Produto p =new Produto(copy,aux[0],aux[1],aux[2],aux[3],aux[4],aux[5]);
                p.setEANOriginal(aux[6]);
                //marca e aux[1]

                if(auchanMap.containsKey(aux[1])) {
                    List<Produto> lii = auchanMap.get(aux[1]);
                    lii.add(p);
                    auchanMapEAN.put(aux[6],p);
                }
                else{
                    List<Produto> lii2 = new ArrayList<>(20);
                    lii2.add(p);
                    auchanMap.put(aux[1],lii2);
                    auchanMapEAN.put(aux[6],p);

                }





                qts++;
            }
            myReader.close();
        } catch (FileNotFoundException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }

        //kappa=0;
        //LER OS DO 2o CSV e por num HASHMAP
        try {
            String path_2oCSV="./"+_2oCSV;
            File myObj2 = new File(path_2oCSV);
            Scanner myReader2 = new Scanner(myObj2);
            String data2 = myReader2.nextLine();
            while (myReader2.hasNextLine()) {
                data2 = myReader2.nextLine();
                String copy2 = data2.toUpperCase();
                String aux2[] = copy2.split(",");
                //System.out.println(copy2);
                Produto p;

                if(aux2.length>6 || aux2.length < 5){
                    continue;
                }

                // 0     1      2            3            4  5
                //Nome,Marca,Quantidade,  PreçoPrimário,Ppu,Promo

                kappa=0;
               if(aux2[0].isEmpty() || aux2[1].isEmpty() || aux2[3].isEmpty() )
                   continue;

                /*

               try{
                   p = new Produto(copy2,aux2[0],aux2[1],aux2[2],aux2[3],aux2[4],aux2[5]);
               }catch (Exception e){
                   continue;
               }
                 */

                if(aux2.length<6){
                     p = new Produto(copy2,aux2[0],aux2[1],aux2[2],aux2[3],aux2[4]);
                }else{
                     p = new Produto(copy2,aux2[0],aux2[1],aux2[2],aux2[3],aux2[4],aux2[5]);
                }

                //marca e aux[1]

                if(secondMap.containsKey(aux2[1])) {
                    List<Produto> lii2 = secondMap.get(aux2[1]);
                    lii2.add(p);
                }
                else{
                    List<Produto> lii22 = new ArrayList<>(20);
                    lii22.add(p);
                    secondMap.put(aux2[1],lii22);

                }

                qts++;
            }
            myReader2.close();
        } catch (FileNotFoundException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }


        //kappa=0;



        //associar or EANS do auchan ao 2o CSV
       for(String ma : auchanMap.keySet()){
           if(secondMap.containsKey(ma)){
               List<Produto> list_auchan = auchanMap.get(ma);
               List<Produto> list_2ndSUPER = secondMap.get(ma);

               for(Produto p1:list_auchan){
                   for(Produto p2:list_2ndSUPER){
                       boolean barata = podeSerOMesmo(p1,p2);
                       if(barata){
                           //System.out.println("\n");
                           //System.out.println(p2.toString() + "\n pode ser igual a \n"+ p1.toString());
                           p2.addEANCopiado(p1.getEANOriginal());
                       }
                   }
               }

           }
       }



       //Escrever para OUTPUT.csv os produtos com EANS encontrados
        try {
            String nomeFileOutput= "OUTPUT"+_2oCSV;
            FileWriter writer = new FileWriter(nomeFileOutput);

            for(List<Produto> ll : secondMap.values() ){
                for(Produto p : ll){
                    int num_eans=p.getEANCopiados().size();
                    int qual=1;
                    writer.write(p.getStrToda());
                    writer.write("[");
                    for(String ean:p.getEANCopiados()){
                        if(qual==num_eans){
                            writer.write(ean);
                        }else{
                            writer.write(ean);
                            writer.write(",");
                            qual++;
                        }
                    }
                    writer.write("]");
                    writer.write("\n");
                }
            }
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }






        //Ver se a funcao podeSer funcemina
        /*
        List<Produto> lalalaa = auchanMap.get("MOURA");
        List<Produto> lblblb  = secondMap.get("MOURA");
        for(Produto p1:lalalaa) {
            for(Produto p2 : lblblb){
                boolean barata = podeSerOMesmo(p1,p2);
                if(barata){
                    System.out.println("\n\n");
                    System.out.println(p2.toString() + "\n pode ser igual a \n"+ p1.toString());
                    System.out.println("\n\n");
                    //p2.addEANCopiado(p1.getEANOriginal());
                }

            }
        }

         */





        kappa=0;

    }

}
