import pandas as pd
# from sequentiality import Sequentiality
from Sequentiality import Sequentiality
 

class TPCS:
    
  def __init__(self, list_of_timestamps, MAX_LEN_MONTHS, END_OF_TIME, debug=False, return_details=False):
    self.lot= list_of_timestamps
    self.EOT=END_OF_TIME
    self.MAX_LEN_MONTHS=MAX_LEN_MONTHS
    self.seq=Sequentiality()
    self.debug=debug
    self.return_details= return_details
    
    if type(self.EOT)==str:
        pass
        #todo convert to pn date time
    
    if type(self.lot)==str:
       pass
       #todo convert to pn date time
    
    self.lot_mdr=self.make_monthdistance_representation(self.lot)
    self.EOT_mdr=self.make_monthdistance_representation([self.EOT])[0]
    
    if self.debug:

      print("list of timestammps (monthdistance representation)", self.lot_mdr)
      print("End of Time (monthdistance representation)", self.EOT_mdr)
    

  
  def convert_date_to_montly_distance_to_2000(self,d):
     origin=pd.to_datetime("01-2020")
     
     r=self.find_diff_in_months(d,origin )
     return r

  def find_diff_in_months(self, a, b):
    # Compute year and month differences
    year_diff = a.year - b.year
    month_diff = a.month - b.month
    
    total_months = year_diff * 12 + month_diff
    
    if a.day < b.day:
        total_months -= 1

    
    if self.debug:
        print("a:", a, "b:", b)
        print("year_diff:", year_diff, "month_diff:", month_diff)
        print("total_months:", total_months)
        
    return total_months
  



  def make_monthdistance_representation(self, list_of_timestamps):

        monthdistance_representation=[]
        for e in list_of_timestamps:
            
            r=self.convert_date_to_montly_distance_to_2000(e)
            
            monthdistance_representation.append(r)
        return monthdistance_representation



  def calculate_LCS_m(self):
    return self.seq.find_LongestConseqSubseq( self.lot_mdr)

  def calculate_LCS_m_1n(self):
    return self.seq.find_LongestConseqSubseq_1gap( self.lot_mdr)

  def calculate_LCS_m_2n(self):
    return self.seq.find_LongestConseqSubseq_2gap( self.lot_mdr)

  def calculate_LCS_m_from_end_of_signal(self):
    return self.seq.find_LongestConseqSubseq_from_end( self.lot_mdr)

  def calculate_LCS_m_from_end_of_signal_1n(self):
    return self.seq.find_LongestConseqSubseq_from_end_with_1_gap( self.lot_mdr)

  def calculate_LCS_m_from_end_of_signal_2n(self):
    return self.seq.find_LongestConseqSubseq_from_end_with_2_gap( self.lot_mdr)

  def calculate_LCS_m_from_end_of_time(self ):
    if self.lot_mdr[-1]!=self.EOT_mdr:
        self.lot_mdr.append(self.EOT_mdr)
       
    r=self.seq.find_LongestConseqSubseq_from_end( self.lot_mdr)
 

    return r

  def calculate_LCS_m_from_end_of_time_1n(self ):
    if self.lot_mdr[-1]!=self.EOT_mdr:
        self.lot_mdr.append(self.EOT_mdr)
    return self.seq.find_LongestConseqSubseq_from_end_with_1_gap( self.lot_mdr)
     


  def calculate_features(self):

      f0=self.calculate_LCS_m()
      f1=self.calculate_LCS_m_1n()
      f2=self.calculate_LCS_m_2n()
      f3=self.calculate_LCS_m_from_end_of_signal()
      f4=self.calculate_LCS_m_from_end_of_signal_1n()
      f5=self.calculate_LCS_m_from_end_of_signal_2n()
      f6= self.calculate_LCS_m_from_end_of_time()
      f7= self.calculate_LCS_m_from_end_of_time_1n()

      contiguity_features=[f0,f1,f2]
      consistency_features=[f3,f4,f5]
      recent_contiguity_features=[f6,f7]
      
      if self.debug:
        
        
        print("LCS:", f0)
        print("LCS 1n:", f1)
        print("LCS 2n:", f2)
        print("LCS from end:", f3)
        print("LCS from end of signal 1n:", f4)
        print("LCS from end of signal 2n:", f5)
        print("LCS from end of time:", f6)
        print("LCS from end of time 1n :", f7)
          
          

      
      return contiguity_features, recent_contiguity_features, consistency_features

    
  def calculate_TPCS(self,  weights=None, printing=True):

      contiguity_features,\
      recent_contiguity_features,\
      consistency_features  =self.calculate_features()
      
      num_of_samples=len(self.lot)
      
      if weights:
        pass
      else:
        weights={ "contiguity_score":1,
                  "recent_contiguity_score":1,
                  "consistency_score":1,
                  "intra_consistency_score":1

        }
      denominator=sum(weights.values())
      
      avg_contiguity_points=        sum(contiguity_features)/len(contiguity_features)
      avg_recent_contiguity_points= sum(recent_contiguity_features)/len(recent_contiguity_features)
      avg_consistency_points=       sum(consistency_features)/len(consistency_features)
      
      
      contiguity_score=       round( avg_contiguity_points/self.MAX_LEN_MONTHS* 5  ,2)
      recent_contiguity_score=round( avg_recent_contiguity_points/self.MAX_LEN_MONTHS* 5,2)
      consistency_score=      round( avg_consistency_points/self.MAX_LEN_MONTHS* 5     ,2)
      intra_consistency_score= round(avg_consistency_points/num_of_samples* 5    ,2)

      
      weighted_contiguity_score       = round(contiguity_score*+weights["contiguity_score"],2)
      weighted_recent_contiguity_score= round(recent_contiguity_score*+weights["recent_contiguity_score"],2)
      weighted_consistency_score      = round(consistency_score*+weights["consistency_score"],2)
      weighted_intra_consistency_score= round(intra_consistency_score*+weights["intra_consistency_score"],2)

      if self.debug:

          
           print("avg_contiguity_points:", avg_contiguity_points)
           print("avg_recent_contiguity_points:", avg_recent_contiguity_points)
           print("avg_consistency_points:", avg_consistency_points)
           print("  ")
           
           print("contiguity_score:", contiguity_score)
           print("recent_contiguity_score:", recent_contiguity_score)
           print("consistency_score:", consistency_score)
           print("intra_consistency_score:", intra_consistency_score)
           print("  ")

           print("weights of contiguity_score:",weights["contiguity_score"])
           print("weights of recent_contiguity_score:",weights["recent_contiguity_score"])
           print("weights of consistency_score:",weights["consistency_score"])
           print("weights of intra_consistency_score:",weights["intra_consistency_score"])
           print("  ")

          
           print("weighted_contiguity_score:", weighted_contiguity_score)
           print("weighted_recent_contiguity_score:", weighted_recent_contiguity_score)
           print("weighted_consistency_score:", weighted_consistency_score)
           print("weighted_intra_consistency_score:", weighted_intra_consistency_score)
           
           
      time_features=(consistency_score, intra_consistency_score, contiguity_score, recent_contiguity_score)
      
      
      weigted_time_features=(weighted_consistency_score, weighted_intra_consistency_score,
                             weighted_contiguity_score,weighted_recent_contiguity_score )
       
      tpcs= sum(weigted_time_features) /denominator
      tpcs= round(tpcs,2)
      

      if printing:
        
        print("--------------:")
        print("Metrics:")
        print(" ")
        print("Contiguity :",contiguity_score)
        print("Recent_contiguity:",recent_contiguity_score)
        print("cconsistency :",consistency_score)
        print("Intra consistency :",intra_consistency_score)
        print("TPCS (weighted avg of all) :",tpcs)
      
      tpcs_details={
                "consistency": consistency_score,
                "intra_consistency":  intra_consistency_score,
                "contiguity": contiguity_score,
                "recent_contiguity":  recent_contiguity_score,
                "weighted_consistency":weighted_consistency_score,
                "weighted_intra_consistency":  weighted_intra_consistency_score,
                "weighted_contiguity": weighted_contiguity_score,
                "weighted_recent_contiguity":  weighted_recent_contiguity_score

                    }
       
      if self.return_details:
           return tpcs,tpcs_details

      else:
          return tpcs
