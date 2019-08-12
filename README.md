# binFilter

1. get no-repeat positions and repeat positions from **dna_rm** file, generate ```.repeat.bed```and ```.norepeat.bed```file

   ```shell
   python getBedNoRepeatFromFa.py ~/xufeng/maize_catalog/genome_and_gff_and_gtf/Zea_mays.AGPv3.25/Zea_mays.AGPv3.25.dna_rm.toplevel.fa.gz
   ```

2. get **bed** file from **mergbin_info_all.txt**, generate ```mergbin_info_all.bed```

   ```shell
   sed '1d' ../binHeatmap/data/mergbin_info_all.txt | awk 'BEGIN{OFS="\t"}{print $2,$3,$4,$1}' > mergbin_info_all.bed
   ```

3. make approximation for the **mergbin_info_all.txt** file, generate ```mergbin_info_all.approx.bed```

   ```shell
   python approxPos.py mergbin_info_all.bed > mergbin_info_all.approx.bed
   ```

4. get overlap from **mergbin_info_all.bed** and **.repeat.bed**, generate ```newBin_200bp.bed``` and the plot ```Bins length distribution(200bp).pdf```

   ```shell
   python getOverlapFileFromBinAndRepeat.py mergbin_info_all.bed Zea_mays.repeat.bed
   ```

5. get ```major``` and ```minor``` information from **.hmp.txt**, generate ```hapmap2maf.txt```

   ```python
   python getMAFfromhapmap.py all_4_data_indep_45576_v3.sort.hmp.txt
   ```

6. make ```bed``` file from ```hapmap2maf.txt```, generate ```hapmap2maf.bed```

   ```shell
   awk 'BEGIN{OFS="\t"}{if($7>=0.15 && $7<=0.35){print $2,$3-1,$3,$1,$7}}' hapmap2maf.txt > hapmap2maf.bed
   ```

7. get the SNP info which ```hapmap2maf.bed``` overlapped with ```newBin_200bp.bed```, generate ```newBin_200bp.hapmap2maf.txt```

   ```shell
   python approxPos.py newBin_200bp.bed | bedtools intersect -a - -b hapmap2maf.bed -wa -wb > newBin_200bp.hapmap2maf.txt
   ```

8. intersect ```mergbin_info_all.approx.bed``` and ```newBin_200bp.hapmap2maf.txt``` to generate the final SNPs in no-repeat bins, **indepSNPinFilterBin.txt** , **indepSNPinFilterBin.bed** and responding **indepSNPinFilterBin.fa**

   ```shell
   bedtools intersect -a mergbin_info_all.approx.bed -b newBin_200bp.hapmap2maf.txt -wa -wb > indepSNPinFilterBin.txt
   awk 'BEGIN{OFS="\t"}{print $9,$11-50,$11+50,$12}' indepSNPinFilterBin.txt > indepSNPinFilterBin.bed
   bedtools getfasta -fi ~/xufeng/maize_catalog/genome_and_gff_and_gtf/Zea_mays.AGPv3.25/Zea_mays.AGPv3.25.dna.genome.fa -bed indepSNPinFilterBin.bed -name -fo indepSNPinFilterBin.fa
   ```

9. make blat with different genome file

   ```shell
   blat GCA_001644905.2_Zm-W22-REFERENCE-NRGENE-2.0_genomic.fna indepSNPinFilterBin.fa -out=blast8 blat/W22.B73.indepSNPs.blat.result_blast8.txt &
   blat Zm-B104-DRAFT-ISU_USDA-0.1.fa indepSNPinFilterBin.fa -out=blast8 blat/B104.B73.indepSNPs.blat.result_blast8.txt &
   blat Zm-CML247-DRAFT-PANZEA-1.0.fasta indepSNPinFilterBin.fa -out=blast8 blat/CML127.B73.indepSNPs.blat.result_blast8.txt &
   blat Zm-Mo17-REFERENCE-CAU-1.0.fsa indepSNPinFilterBin.fa -out=blast8 blat/Mo17.B73.indepSNPs.blat.result_blast8.txt &
   blat Zm-PH207-REFERENCE_NS-UIUC_UMN-1.0.fasta indepSNPinFilterBin.fa -out=blast8 blat/PH207.B73.indepSNPs.blat.result_blast8.txt &
   ```

10. filter blat result by identity and fetch the top5 results

    ```shell
    python filterBlatByIdentity.py blat/W22.B73.indepSNPs.blat.result_blast8.txt 1>blat/W22.B73.indepSNPs.levels.txt 2>blat/W22.B73.indepSNPs.top.txt
    python filterBlatByIdentity.py blat/B104.B73.indepSNPs.blat.result_blast8.txt 1>blat/B104.B73.indepSNPs.levels.txt 2>blat/B104.B73.indepSNPs.top.txt
    python filterBlatByIdentity.py blat/CML127.B73.indepSNPs.blat.result_blast8.txt 1>blat/CML127.B73.indepSNPs.levels.txt 2>blat/CML127.B73.indepSNPs.top.txt
    python filterBlatByIdentity.py blat/Mo17.B73.indepSNPs.blat.result_blast8.txt 1>blat/Mo17.B73.indepSNPs.levels.txt 2>blat/Mo17.B73.indepSNPs.top.txt
    python filterBlatByIdentity.py blat/PH207.B73.indepSNPs.blat.result_blast8.txt 1>blat/PH207.B73.indepSNPs.levels.txt 2>blat/PH207.B73.indepSNPs.top.txt
    
    ```


11. get the SNP numbers in different genome and different identity

    ```shell
    join blat/Mo17.B73.indepSNPs.levels.txt <(join blat/PH207.B73.indepSNPs.levels.txt <(join blat/CML127.B73.indepSNPs.levels.txt <(join blat/W22.B73.indepSNPs.levels.txt blat/B104.B73.indepSNPs.levels.txt))) 
    ```

12. get final 5 genome overlapped SNP info

    ```shell
    comm -12 <(sort blat/PH207.B73.indepSNPs.top.txt) <(comm -12 <(sort blat/Mo17.B73.indepSNPs.top.txt) <(comm -12 <(sort blat/CML127.B73.indepSNPs.top.txt) <(comm -12 <(sort blat/W22.B73.indepSNPs.top.txt) <(sort blat/B104.B73.indepSNPs.top.txt)))) | sort -u > 5_genome_overlap_SNPs.txt
    ```

    

