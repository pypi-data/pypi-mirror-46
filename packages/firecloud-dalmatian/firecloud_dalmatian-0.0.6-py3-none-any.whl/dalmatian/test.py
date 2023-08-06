import pandas as pd
import imp
import dalmatian

# imp.reload(dalmatian.core); imp.reload(dalmatian.wmanager); imp.reload(dalmatian);

test_wm = dalmatian.WorkspaceManager('broad-firecloud-gtex/dalmatian_test_0718')
test_wm.create_workspace()

upload_df = pd.DataFrame(np.array([
    ['participant1', 'participant1', 'participant2', 'participant2'],
    ['all_samples', 'all_samples', 'all_samples', 'all_samples'],
    ['a','b','c','d'],
    ['aa','bb','cc','dd']
]).T, index=['sample1', 'sample2', 'sample3', 'sample4'], columns=['participant', 'sample_set_id', 'attr1', 'attr2'])
upload_df = upload_df[['sample_set_id', 'participant', 'attr1', 'attr2']]
upload_df.index.name = 'sample_id'
# upload_df['fastq1'] = 4*[['gs://path1', 'gs://path2']]
# upload_df['fastq1'] = 4*['gs://path1, gs://path2']
test_wm.upload_samples(upload_df, add_participant_samples=False)

test_wm.update_sample_attributes({'Tumor':'tumor_sample', 'Normal':'normal_sample'}, 'sample1')
test_wm.delete_entity_attributes('sample', test_wm.get_samples()['Normal'])
test_wm.delete_entity_attributes('sample', test_wm.get_samples()[['Normal', 'Tumor']])
test_wm.delete_entity_attributes('sample', ['Tumor', 'Normal'], entity_id='sample1')

test_wm.update_sample_attributes(pd.Series(data=['Normal', 'Tumor', 'Normal', 'Tumor'], index=['sample1', 'sample2', 'sample3', 'sample4'], name='sample_type'))
test_wm.make_pairs()
test_wm.update_entity_set('pair', 'pair_set_test', ['sample2-sample1', 'sample4-sample3'])

test_wm.get_pair_sets()
test_wm.get_pairs_in_pair_set('pair_set_test')


test_wm.update_participant_samples_and_pairs()
test_wm.get_participants()
test_wm.get_pairs()

test_wm.delete_sample_set('all_samples')
test_wm.delete_sample('sample4')
test_wm.delete_participant('participant1')
test_wm.delete_participant('participant1', delete_dependencies=True)
test_wm.delete_entity_attributes('sample', test_wm.get_samples()['attr2'])
test_wm.update_sample_set('all_samples', test_wm.get_samples().index)

test_wm.import_config('broadinstitute_gtex', 'star_v1-0_BETA_cfg')

test_wm.delete_workspace()

test_wm.import_config('broadinstitute_gtex','rsem_v1-0_BETA_cfg')
attr = test_wm.get_config('broadinstitute_gtex','rsem_v1-0_BETA_cfg')
attr['name'] = 'rsem_v1-0_BETA_cfg_copy'
attr['inputs']['rsem_workflow.rsem.memory'] = '26'
attr['inputs']['rsem_workflow.rsem.num_threads'] =  '4'
test_wm.update_configuration(attr)


# import fcsettings
# attr = fcsettings.get_config_attributes('cram_to_bam', 'francois', 'cram_to_bam_v1-0_BETA')
# test_wm.update_configuration(attr)
# test_wm.publish_config('francois', 'cram_to_bam_v1-0_BETA', to_cnamespace='francois', to_config='cram_to_bam_v1-0_BETA_cfg', public=True)


