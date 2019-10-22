import kfp

def task(volume,
         step_name='c_task'
         ):
    
    return kfp.dsl.ContainerOp(
        name=step_name,
        image='rochanmehrotra/testing_kf:c_prog',
        command=['python3', '/component/src/runner.py'],
        pvolumes={mount_output_to: volume}
    )

@kfp.dsl.pipeline(name='c pipeline', description='')
def mlp_pipeline(
        rok_url,
        pvc_size='1Gi'):
    
    vop = kfp.dsl.VolumeOp(
        name='create-volume',
        resource_name='c_pipeline',
        annotations={"rok/origin": rok_url},
        size=pvc_size
    )
    
    component_1 = task(
        volume=vop.volume
    )
    
    if __name__ == '__main__':
         import kfp.compiler as compiler
         compiler.Compiler().compile(mlp_pipeline, 'c_pipeline.tar.gz')
